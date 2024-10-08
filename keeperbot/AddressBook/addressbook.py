from collections import UserDict
from typing import Union
from datetime import datetime
from colorama import Fore, Style, init
from .record import Record, Note

init(autoreset=True)

class AddressBook(UserDict):
    """Class for storing and managing contact records."""
    
    def get_owner(self) -> Union[Record, None]:
        for record in self.data.values():
            if getattr(record, 'owner', False) == True:
                return record
        return None
        
    def add_record(self, record: Record) -> None:
        """Add a record to the address book.

        Args:
            record (Record): The record to be added.

        Raises:
            ValueError: If the record is invalid.
        """
        if not isinstance(record, Record) or not record.name.value:
            raise ValueError(f"{Fore.RED}Invalid record.{Style.RESET_ALL}")
        self.data[record.name.value] = record

    def find_phone(self, phone: str) -> Union[Record, None]:
        """Find a contact by phone number.

        Args:
            phone (str): The phone number to search for.

        Returns:
            Union[str, None]: The record of the first found contact, or None if not found.
        """
        # TODO: Refactor this method to return a list of records with the same phone number.
        for record in self.data.values():
            for number in record.phones:
                if phone == number.value:
                    return record
        return None

    def find_contact(self, name: str) -> Union[Record, None]:
        """Find a record by name.

        Args:
            name (str): The name to search for.

        Returns:
            Union[Record, None]: The found record, or None if not found.
        """
        return self.data.get(name, None)

    def delete(self, name: str) -> None:
        """Delete a record by name.

        Args:
            name (str): The name of the record to delete.

        Raises:
            ValueError: If the record is not found or the name is invalid.
        """
        if name in self.data:
            del self.data[name]
            return 'Contact deleted.'
        else:
            raise ValueError(
                f"{Fore.RED}Record not found or invalid name.{Style.RESET_ALL}"
            )

    def get_upcoming_birthdays(self, n_days: int=0):
        """
        Function returns a list of dictionaries with users and
        their birthdays for n days from today.

        Args:
            n_days: the number of days to check for upcoming birthdays form today.
        Return:
            upcoming_birthdays: a list of records with users who celebrate birthday this in n_days.
        """
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days
                
                if 0 <= delta_days <= n_days:
                    upcoming_birthdays.append(record)

        return upcoming_birthdays

    def find_contacts_by_field(self, field_name: str, value: any):
        """Find a record by field name.
        Args:
            field_name (str): The field to search for.
            value (any): The value to search for.
        Returns:
           list: The found records.
        """

        result = set()
        for item in self.data.values():
            if field_name == "phone" or field_name == "phones":
                if value in item.phones or any([value in phone.__str__() for phone in item.phones]):
                    result.add(item)
            elif field_name == "note":
                if value in item.notes or any([value.lower() in note.__str__().lower() for note in item.notes]):
                    result.add(item)
            elif field_name == "tag":
                if item.notes:
                    for note in item.notes:
                        if any([value.lower() in tag.__str__().lower() for tag in note.tags]):
                            result.add(item)
                            break
            elif hasattr(item, field_name):
                field_value = getattr(item, field_name)
                if field_value == value or value.lower() in field_value.__str__().lower():
                    result.add(item)
            elif field_name == "all":
                for dict_value in item.__dict__.values():
                    if value == dict_value or value.lower() in dict_value.__str__().lower():
                        result.add(item)
        return list(result)

    def sort_records(self) -> None:
        """Sort the records in the address book by name."""
        sorted_records = sorted(
            self.data.values(), key=lambda record: record.name.value
        )
        self.data = {record.name.value: record for record in sorted_records}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value='{self.value}')"

    def find_note_by_title(self, note_title) -> Union[Note, None]:
        """Find a note by title.

        Args:
            note_title (str): The title to search for.

        Returns:
            Record: The found record, or None if not found.
        """
        for record in self.data.values():
            for note in record.notes:
                if note.title == note_title:
                    return note
        return None

    def delete_note_by_title(self, note_title):
        """Delete a note by title.

        Args:
            note_title (str): The title of the note to delete.

        Raises:
            ValueError: If the note is not found or the title is invalid.
        """
        for record in self.data.values():
            for note in record.notes:
                if note.title == note_title:
                    record.notes.remove(note)
                    return

    def find_notes_by_tag(self, tag):
        """Find notes by tag.

        Args:
            tag (str): The tag to search for.

        Returns:
            list: The found notes.
        """
        result = []
        for record in self.data.values():
            if record.notes:
                for note in record.notes:
                    if tag in note.tags:
                        result.append(note)
        return result

    def update_name(self, name, new_name):
        self.data[new_name] = self.data.pop(name)
        return self.data[new_name].edit_name(new_name)



if __name__ == "__main__":
    field = AddressBook("example value")
    print(field.__doc__)
    for name, func in field.__class__.__dict__.items():
        if callable(func):
            print(name)
            print(func.__doc__)
