# System Design Practice
----
## API Gateway


This service acts as an API gateway, authenticating the user by synchronous communication with the Auth service.

- It reaches out to the Auth service and validates the JWT to check user authorization and permission levels, using this route:

    ``` python
    @server.route("/login", methods=["POST"])
    def login():
        token, err = access.login(request)
        
        if not err:
            return token, 200
        else:
            return err
    ```

- It uploads a video file if the user has access and sends a message rabbitMQ exchange with the topic *"video"* so the video processor can consume this message:
    ``` python
    @server.route("/upload", methods=["POST"])
    def upload():
        access, err = validate.token()
        
        access = json.loads(access)
        
        if access["admin"]:
            if len(request.files) == 1:
                for _, file in request.files.items():
                    err = util.upload(file, fs, channel, access)
                    
                    if err:
                        return err, 500
                    
                return "File uploaded", 200
            else:
                return "Exactly 1 file required", 400
            
        else:
            return "You do not have permission to upload", 401
    ```



 
