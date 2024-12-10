from ast import literal_eval

from openai import OpenAI
from pydantic import BaseModel

from app.dto.responses import TransactionalDetail
from app.exceptions.openai_exceprions import OpenAIResponseError
from config.project_config import settings


class OpenAi(BaseModel):
    api_key: str
    model: str

    def get_details(self, message: str) -> TransactionalDetail:
        client = OpenAI(api_key=self.api_key)

        completion = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": """Ты - ассистент, который определяет название траты, ее цену и категорию исходя из сообщения.
                                              Тебе на вход попадает сообщение о какой-то трате или доходе, например: Я купил булочку за 100 рублей
                                              Ты должен вернуть JSON
                                              {\"name\": \"покупка булочки\",\"price\": 100, \"category\": \"RESTAURANTS\"}
                                              И БОЛЬШЕ НИЧЕГО! ТОЛЬКО JSON И ВСЕ!
                                                

                                              ТРАТЫ:
                                              Ты должен сам определить категорию и вернуть одну из них:
                                              HOTELS, CLOTHING, SUPERMARKETS, RESTAURANTS, SERVICES, DIGITAL, FINANCE, TRIPS,
                                              COSMETICS, OTHER(если ничего другое не подходит), INCOME(когда приходит ЛЮБОЙ доход)
                                              
                                              Все траты переводи в рубли INTEGER!! К доллару считай по курсу 100 к 1
                                              
                                              Правильно формируй JSON, НИЧЕГО КРОМЕ JSON НЕ ПРИСЫЛАЙ МНЕ!
                                              
                                              
                                              ДОХОДЫ:
                                              Ты должен просто убедиться точно, что это доход по деньгам и просто вернуть JSON, например \"Мне пришла зарплата 300К рублей\" 
                                              или мне вернули долг 100р, или я нашел 500 рублей на улице. Любое действие, которое описывает ПОЛУЧЕНИЕ ДЕНЕГ - ЭТО category INCOME!!!
                                              {\"name\": \"зарплата\",\"price\": 300000, \"category\": \"INCOME\"}

                                              
                                              ОБЩИЕ ПРАВИЛА:
                                              -Всегда числовые параметры приводи к целым числам, к INTEGER!
                                              -Если ты не можешь выполнить мою просьбу, то возвращай \"-\" и все!
                                               Например если человек не указал цену или сказал что-то не по теме, пример, что он почитал книгу    
                                              -Внимательно смотри на различия между тратами и доходами(INCOME)!                                                                                                                        
                                              """},
                {"role": "user", "content": message}
            ]
        )

        print(f"{message}   :   {completion.choices[0].message.content}")

        try:
            response_json = literal_eval(completion.choices[0].message.content)

            transactional_detail = TransactionalDetail(**response_json)
            return transactional_detail
        except Exception:
            raise OpenAIResponseError("Невозможно получить детали траты")


openai = OpenAi(api_key=settings.OPENAI_KEY, model=settings.OPENAI_MODEL)
