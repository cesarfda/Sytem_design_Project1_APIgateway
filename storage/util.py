import pika, json

def upload(file, fs, channel, access):
    try:
        file_id = fs.put(file, filename=file.filename)
    except Exception as err:
        return "internal error", 500
    
    message = {
        "video_fid": file_id,
        "mp3_fid": None,
        "username": access["username"]
    }
    
    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except:
        fs.delete(file_id)
        return "internal error", 500