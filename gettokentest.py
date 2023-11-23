import requests
import json

access_token = "5d692352dbcea2d43384a81c7f459de1_0590de3c23fcadafa068dfcb97ff68b4"

def getAccessToken():
    url = "https://www.tistory.com/oauth/access_token?"
    client_id = "68b7368ceec4522809c75ab1a00553ea"
    client_secret = "68b7368ceec4522809c75ab1a00553ea2c78d36135d7f26e02e6d843a5cf43e5755e276f"
    code = "f0a74fd5bad39ce287e7cc8e1fefc7ec04cb6aa5a7c0f4353bd64515eeb2635b77808b71"
    redirect_uri = "https://wzacorn.tistory.com/"
    grant_type="authorization_code" # authorization_code 고정

    data = url
    data += "client_id="+client_id+"&"
    data += "client_secret="+client_secret+"&"
    data += "redirect_uri="+redirect_uri+"&"
    data += "code="+code+"&"
    data += "grant_type="+grant_type
    print(data)
    return  requests.get(data)


def getCategoryID():
    url = "https://wzacorn.tistory.com/apis/category/list?"
    output = "json"
    blogName = "wzacorn"

    data = url
    data += "access_token=" + access_token + "&"
    data += "output=" + output + "&"
    data += "blogName=" + blogName

    print(data)
    return requests.get(data)



if __name__ == "__main__":
    token = getAccessToken().content
    print(token.decode('utf-8'))

