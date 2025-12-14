from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "warnings" DROP COLUMN "warnings";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "warnings" ADD "warnings" INT NOT NULL;"""


MODELS_STATE = (
    "eJztl2Fv2jAQhv8K4tMqdRMNUNi+UbR1VB1MHdsqVVVkEhM8HDu1nRVU8d/ncxIcQpoWad"
    "poxTd47y6+e5L3Ag/1kPuYyncXfI5l/UPtoc5QiPWHzcBxrY6iyMogKDShJvPXOmUilUCe"
    "0uIUUYm15GPpCRIpwplWWUwpiNzTiYQFVooZuYuxq3iA1QwLHbi51TJhPl6YxszXaO5OCa"
    "b+RqPEh7ON7qplZLQzEgyY+mRy4cCJ63Eah8zmR0s142xdQJgCNcAMC6QwnKBEDBNAg+mk"
    "2VBJszYl6TJX4+MpiqnKTfxMDB5ngFB3k9yMAE55+95xms2O02iedtutTqfdbXR1rmlpO9"
    "RZJQNbIMmlDJbB+WA4hkG5vk/J3QNhZWqQQkmV4W0BK7xQ24jHWi0HnOUXEOvBiogzoFWM"
    "M8FCts/W36FcAWz88drgCqW8oyAMf/Su+p97V2++9K6PTGSZRi5Hw/Ms3dId9i9HZ5ovPL"
    "3TeQ4vCBPkze+R8N2tCHf4Y7nbodAJiwpiKDCsYGKYL3XzV4F94gGgUrPnw5WWjwqJB+Mf"
    "jH8w/h4b/ycSTKModf06Vmn5+3zWwe+v0e+xxMLdlXKu6GnU++H7f0nb0hUYSd3nDvvUVh"
    "w26t5t1B4WxJuV7dM0UrlNkc3Zm136ihapc9LqtLrN09ba0WulyshPr8jfWEhS5uL+DIly"
    "ermSl2Jj/dQvXIpZoOABd9rtCmaZi3XWUcGwachJYpvbEKyxA8Q0/WUCPGk0ngFQZz0K0M"
    "Q2AeoTFWYlv88vvo2G5RBzJQWQ35ke8Ab+0h3XKJHqdj+xVlCEqatfL8U3CVDgUgXCXMVc"
    "4L+/XlZ/AMdBLp8="
)
