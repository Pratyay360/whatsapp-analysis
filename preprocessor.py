import pandas as pd
import re
from dateutil import parser


def preprocess(data):
    if not data or not isinstance(data, str):
        print("Input data is invalid (None, empty, or not a string). Returning empty DataFrame.")
        return pd.DataFrame(columns=[
            'date', 'users', 'message', 'year', 'month_num', 'specific_date', 
            'day_name', 'month', 'day', 'hour', 'minute', 'period'
        ])

    # Raw date pattern
    pattern_str = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?(?:\s?[APap][Mm])?\s-\s'
    
    full_date_strings = []
    message_content = []

    # Find dates
    date_matches = list(re.finditer(pattern_str, data))

    if not date_matches:
        print("No date patterns found by finditer. Cannot extract messages. Returning empty DataFrame.")
        return pd.DataFrame(columns=[
            'date', 'users', 'message', 'year', 'month_num', 'specific_date', 
            'day_name', 'month', 'day', 'hour', 'minute', 'period'
        ])

    for i, match in enumerate(date_matches):
        current_date_str = match.group(0)  # Matched date
        
        # Start of message
        start_of_message = match.end()
        
        # End of message: next match or end
        end_of_message = date_matches[i+1].start() if i + 1 < len(date_matches) else len(data)
        
        msg_text = data[start_of_message:end_of_message].strip()
        
        # Add if msg exists
        if msg_text:
            full_date_strings.append(current_date_str)
            message_content.append(msg_text)

    print(f"Total messages extracted (finditer method): {len(message_content)}")
    print(f"Total dates extracted (finditer method): {len(full_date_strings)}")

    if not message_content:
        print("No non-empty messages. Returning empty DataFrame.")
        return pd.DataFrame(columns=[
            'date', 'users', 'message', 'year', 'month_num', 'specific_date', 
            'day_name', 'month', 'day', 'hour', 'minute', 'period'
        ])
    
    # Build DataFrame
    df = pd.DataFrame({"user_message": message_content, "raw_message_date": full_date_strings})
    
    # Parse date safely
    def try_parse_date(date_str_val):
        # Clean date str
        cleaned_date_str = date_str_val.replace(" - ", "").strip()
        try:
            return parser.parse(cleaned_date_str, fuzzy=True, dayfirst=True)
        except Exception:
            try:
                return parser.parse(cleaned_date_str, fuzzy=False, dayfirst=False)
            except Exception as e:
                print(f"Failed to parse date: '{cleaned_date_str}'. Error: {e}")
                return pd.NaT
    
    df["date"] = df["raw_message_date"].apply(try_parse_date)
    
    # Remove parse failures
    df = df.dropna(subset=['date'])
    
    if df.empty:
        print("No valid dates parsed. Returning empty DataFrame.")
        return pd.DataFrame(columns=[
            'date', 'users', 'message', 'year', 'month_num', 'specific_date', 
            'day_name', 'month', 'day', 'hour', 'minute', 'period'
        ])
        
    users_list = []
    messages_list = [] 
    
    # Compile user regex
    user_pattern_re = re.compile(r'^([^:]+?):\s+(.*)', re.DOTALL)

    for um_text in df['user_message']:
        try:
            message_str = str(um_text).strip()  # Ensure string
            
            if not message_str:
                users_list.append('empty_message')
                messages_list.append('')
                continue

            user_match = user_pattern_re.match(message_str)
            
            if user_match:
                username = user_match.group(1).strip()
                msg_content = user_match.group(2).strip()
                users_list.append(username)
                messages_list.append(msg_content)
            else:
                ms_lower = message_str.lower()
                is_group_notification = False
                # Check group notif
                group_notification_keywords = [
                    ("added", "to the group"), ("left",), ("changed the subject",),
                    ("changed this group's icon",), ("changed the group description",),
                    ("messages and calls are end-to-end encrypted",), ("created group",),
                    ("you were added",), ("admin", "promoted"), ("admin", "dismissed"),
                    ("security code changed",), ("joined using this group's invite link",),
                    ("was removed",), ("you're now an admin",)
                ]
                for kw_tuple in group_notification_keywords:
                    if all(kw.lower() in ms_lower for kw in kw_tuple):
                        is_group_notification = True
                        break
                
                if is_group_notification:
                    users_list.append('group_notification')
                    messages_list.append(message_str)
                else:
                    users_list.append('unknown_user')
                    messages_list.append(message_str)
        except Exception as e:
            print(f"Error processing message: '{str(um_text)[:70]}'. Error: {e}")
            users_list.append('error_processing')
            messages_list.append(str(um_text)[:70] + '...' if len(str(um_text)) > 70 else str(um_text))
    
    df['users'] = users_list
    df['message'] = messages_list
    
    # Debug info
    total_df_rows = len(df)
    group_notifications_count = len(df[df['users'] == 'group_notification'])
    actual_user_messages_count = len(df[~df['users'].isin(['group_notification', 'empty_message', 'error_processing', 'unknown_user'])])
    
    print(f"DataFrame rows: {total_df_rows}")
    print(f"Group notif: {group_notifications_count}")
    print(f"Actual user messages: {actual_user_messages_count}")
    
    # Remove temp cols
    df.drop(columns=['user_message', 'raw_message_date'], inplace=True, errors='ignore')
    
    # Extract time parts
    df["year"] = df["date"].dt.year
    df['month_num'] = df["date"].dt.month
    df['specific_date'] = df["date"].dt.date
    df['day_name'] = df["date"].dt.day_name()
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute
    
    # Hour period
    period = []
    for hour_val in df["hour"]:
        if hour_val == 23:
            period.append("23-00")  # 23->00
        elif hour_val == 0:
            period.append("00-01")  # 00->01
        else:
            period.append(f"{hour_val:02d}-{(hour_val + 1):02d}")  # Format hours
    df['period'] = period
    
    return df
