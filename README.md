# SingleMeaning  
 
Веб-сервис (по умолчанию **host='127.0.0.1'**, **port=8090**), принимающий POST запрос с методом *check*  и списком предложений в теле (json) 
Принимает два предложения, возвращает **True** если процент схожести между превышает 50%, в противном случае **False**  

**Пример url**: 127.0.0.1:8090/check  
**Пример json**:   
```json
{
  "data": 
    [
    "Data science is awesome",
    "machine learning is interesting"]
}
```

*Примечание: 
nltk.download('wordnet')
nltk.download('stopwords')*
