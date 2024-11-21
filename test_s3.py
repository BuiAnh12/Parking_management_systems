from s3_sender.sender import S3Uploader 

file_path = "./output/detected_frame_human_17292.jpg"  # Replace with the path to your file

# Create an instance of S3Uploader
uploader = S3Uploader()

# Upload the file
uploader.upload_picture(file_path)