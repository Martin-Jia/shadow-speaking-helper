class Funcs {
    static getToken() {
        token = localStorage.getItem("access-token")
        if (token == null){
            return null
        }
        this.validateToken(token)
        .then((value) => {
            if (value['error']) {
                token = null
            }
        })
        .catch((error) => {
            token = null
        })
        return token
    }

    static async validateToken(token) {
        if (!token) {
            throw Error("token mush not be empty");
        }
        let response = await fetch(Constants.apiEndPoint + "/verifyToken", {
            method: 'GET', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, *cors, same-origin
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, *same-origin, omit
            headers: {
              'access-token': token
              // 'Content-Type': 'application/x-www-form-urlencoded',
            },
          })
        return response.json()
    }
}

class Constants {
    static apiEndPoint = "http://localhost:3600"
}