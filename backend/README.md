## API(KosenNote) のルール

基本フォーマット
``` python
Response({"status": "success", "data": data}, status=status.HTTP_200_OK)
# or
Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
```

### dataの中身
success
``` json
{
    "status": "success",
    "data": {
        "somedata" : samedata,
        "somedata2" : samedata2,
    }
}
```

error
``` json
{
    "status": "error",
    "data": {
        "error" : "error",
        "error_message" : "error message"
    }
}
```

### errorメッセージ一覧

|エラーの種類|エラーメッセージ|exceptionの場所|説明|
|-|-|-|-|
|DoesNotExist|オブジェクト名 DoesNotExist|オブジェクト名.DoesNotExist|検索したオブジェクトが存在しない|
|SomethingWrong|SomethingWrong|--|不明のエラー|
|FailureAuthentication|FailureAuthentication|--|認証失敗|
|AlreadyExists|AlreadyExists|IntegrityError|既に存在したオブジェクト|
|Expired|Expired|--|失効したオブジェクト|
|KeyError|KeyError|--|必要なオブジェクト|



\
\
\
\
\
\
\
\
\

\
\
\
\
\
\\
\
/
/
/
/
/