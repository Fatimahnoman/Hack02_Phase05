import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dateutil import parser as date_parser


class IntentParser:
    """Parser for extracting intents and entities from natural language commands."""
    
    def __init__(self):
        # Define regex patterns for various intents
        self.patterns = {
            'set_priority': r'(make|set).*?(high|medium|low).*?priority',
            'add_tag': r'#(\w+)|tag.*?#(\w+)',
            'set_due_date': r'(by|on|before)\s+(.+?)(?:\s|$)',
            'set_reminder': r'(remind|reminder).*?(in|at|on)\s+(.+?)(?:\s|$)',
            'create_recurring': r'(every|daily|weekly|monthly|recurring).*?(task|todo)',
            'create_task': r'(create|add|make).*?(task|todo|note)',
        }
    
    def parse_intent(self, text: str) -> Dict:
        """Parse the intent and extract entities from the natural language text."""
        text_lower = text.lower().strip()
        result = {
            'intent': None,
            'entities': {},
            'original_text': text
        }
        
        # Check for different intents
        if re.search(self.patterns['set_priority'], text_lower):
            match = re.search(self.patterns['set_priority'], text_lower)
            if match:
                result['intent'] = 'set_priority'
                result['entities']['priority'] = match.group(2)
        
        if re.search(self.patterns['add_tag'], text_lower):
            matches = re.findall(self.patterns['add_tag'], text_lower)
            if matches:
                result['intent'] = 'add_tag'
                # Flatten the tuple results from regex groups
                tags = [tag for group in matches for tag in group if tag]
                if not tags:
                    # If the regex didn't capture properly, try alternative extraction
                    tags = re.findall(r'#(\w+)', text_lower)
                result['entities']['tags'] = tags
        
        if re.search(self.patterns['set_due_date'], text_lower):
            match = re.search(self.patterns['set_due_date'], text_lower)
            if match:
                result['intent'] = 'set_due_date'
                date_text = match.group(2)
                parsed_date = self.parse_date(date_text)
                if parsed_date:
                    result['entities']['due_date'] = parsed_date
        
        if re.search(self.patterns['set_reminder'], text_lower):
            match = re.search(self.patterns['set_reminder'], text_lower)
            if match:
                result['intent'] = 'set_reminder'
                time_text = match.group(3)
                parsed_time = self.parse_time(time_text)
                if parsed_time:
                    result['entities']['reminder_time'] = parsed_time
        
        if re.search(self.patterns['create_recurring'], text_lower):
            result['intent'] = 'create_recurring'
            # Extract recurrence pattern
            result['entities']['recurrence_pattern'] = self.extract_recurrence_pattern(text_lower)
        
        # If no specific intent matched, check if it's a task creation
        if result['intent'] is None and re.search(self.patterns['create_task'], text_lower):
            result['intent'] = 'create_task'
        
        # If still no intent, treat as general task creation
        if result['intent'] is None:
            result['intent'] = 'create_task'
        
        # Extract additional entities that might be present regardless of intent
        result['entities'].update(self.extract_additional_entities(text))
        
        return result
    
    def parse_date(self, date_text: str) -> Optional[datetime]:
        """Parse date from text using dateutil."""
        try:
            # Use dateutil to parse the date
            parsed_date = date_parser.parse(date_text, fuzzy=True)
            return parsed_date
        except:
            # If parsing fails, try to extract relative dates like "tomorrow", "next week"
            now = datetime.now()
            if 'tomorrow' in date_text:
                return now + timedelta(days=1)
            elif 'next week' in date_text:
                return now + timedelta(weeks=1)
            elif 'next month' in date_text:
                # Approximate: add 30 days
                return now + timedelta(days=30)
            elif 'today' in date_text:
                return now
            return None
    
    def parse_time(self, time_text: str) -> Optional[datetime]:
        """Parse time from text."""
        try:
            # Use dateutil to parse the time
            parsed_time = date_parser.parse(time_text, fuzzy=True)
            return parsed_time
        except:
            return None
    
    def extract_recurrence_pattern(self, text: str) -> Dict:
        """Extract recurrence pattern from text."""
        pattern = {
            'recurrence_type': 'daily',  # default
            'interval': 1,
            'weekdays_mask': None
        }
        
        text_lower = text.lower()
        
        if 'daily' in text_lower:
            pattern['recurrence_type'] = 'daily'
        elif 'weekly' in text_lower:
            pattern['recurrence_type'] = 'weekly'
            # Try to extract specific days
            days_map = {'monday': 2, 'tuesday': 4, 'wednesday': 8, 'thursday': 16, 'friday': 32, 'saturday': 64, 'sunday': 1}
            weekdays_mask = 0
            for day, bit in days_map.items():
                if day in text_lower:
                    weekdays_mask |= bit
            if weekdays_mask:
                pattern['weekdays_mask'] = weekdays_mask
        elif 'monthly' in text_lower:
            pattern['recurrence_type'] = 'monthly'
        elif 'custom' in text_lower or ('every' in text_lower and 'days' in text_lower):
            pattern['recurrence_type'] = 'custom'
            # Extract interval if specified
            interval_match = re.search(r'every\s+(\d+)\s+days?', text_lower)
            if interval_match:
                pattern['interval'] = int(interval_match.group(1))
        
        return pattern
    
    def extract_additional_entities(self, text: str) -> Dict:
        """Extract additional entities that might be present in the text."""
        entities = {}
        
        # Extract priority if mentioned
        priority_match = re.search(r'(high|medium|low).*?priority', text.lower())
        if priority_match:
            entities['priority'] = priority_match.group(1)
        
        # Extract tags
        tag_matches = re.findall(r'#(\w+)', text.lower())
        if tag_matches:
            entities['tags'] = tag_matches
        
        return entities


# Example usage:
# parser = IntentParser()
# result = parser.parse_intent("Create a high priority task #work to buy groceries by tomorrow")
# print(result)