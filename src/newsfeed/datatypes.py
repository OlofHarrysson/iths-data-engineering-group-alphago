from datetime import date, datetime

import pydantic


# Note: The code below uses Python type hints to clarify the variable types.
# More info: https://realpython.com/lessons/type-hinting/
class BlogInfo(pydantic.BaseModel):
    unique_id: str
    title: str
    description: str
    link: str
    blog_text: str
    published: date
    timestamp: datetime

    def get_filename(self):
        filename = f'{self.title.replace(" ", "_")}.json'
        #  if filename.endswith(".json.json"):
        #     filename = filename.replace()
        return filename


class BlogSummary(pydantic.BaseModel):
    unique_id: str  # This should be the same as for BlogInfo so that they can be linked
    title: str
    text: str

    def get_filename(self):
        return f'{self.title.replace(" ", "_")}.json'
