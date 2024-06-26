import matplotlib
matplotlib.use("Agg")  
import cv2
import numpy as np

import urllib.request
import os
import sys
import ast
import logging
import requests as req
import paramiko


def scale_and_save_image(image_url, target_size, output_folder):
	try:
		response = urllib.request.urlopen(image_url)
		img_array = np.array(bytearray(response.read()), dtype=np.uint8)
		original_image = cv2.imdecode(img_array, -1)

		scale_factor = min(target_size[1] / original_image.shape[1], target_size[0] / original_image.shape[0])
		new_size = (int(original_image.shape[1] * scale_factor), int(original_image.shape[0] * scale_factor))
		scaled_image = cv2.resize(original_image, new_size, interpolation=cv2.INTER_LANCZOS4)

		canvas = np.zeros((target_size[0], target_size[1], 3), dtype=np.uint8)
		canvas.fill(255)

		x_offset = (canvas.shape[1] - scaled_image.shape[1]) // 2
		y_offset = (canvas.shape[0] - scaled_image.shape[0]) // 2
		canvas[y_offset:y_offset + scaled_image.shape[0], x_offset:x_offset + scaled_image.shape[1]] = scaled_image

		folder_path = os.path.join(output_folder, f"{target_size[0]}x{target_size[1]}")


		remote_image_path = os.path.join(folder_path, f"{isbn}.jpg")
		image_bytes = cv2.imencode('.jpg', canvas)[1].tobytes()
  
		ssh_client_1 = paramiko.SSHClient()
		ssh_client_1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_client_1.connect("194.58.104.214", 22, "root", "J$@F+*Ep*j3y")
		sftp_1 = ssh_client_1.open_sftp()
		with sftp_1.file(remote_image_path, 'wb') as remote_file:
			remote_file.write(image_bytes)
		sftp_1.close()
		ssh_client_1.close()

		ssh_client_2 = paramiko.SSHClient()
		ssh_client_2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_client_2.connect("194.58.121.225", 22, "root", "iTciJg4A4qz?")
		sftp_2 = ssh_client_2.open_sftp()
		with sftp_2.file(remote_image_path, 'wb') as remote_file:
			remote_file.write(image_bytes)
		sftp_2.close()
		ssh_client_2.close()

		req.post("http://api_gateway:5000/api/working_data/photo_found", json={f"{isbn}" : f"{remote_image_path}"})
  
		logging.info(f"Изображение {image_url} успешно масштабировано и сохранено как {remote_image_path}")
	except Exception as e:
		logging.error(f"Произошла ошибка: {e} - Изображение: {image_url}")

if __name__ == "__main__":
    logging.basicConfig(filename='./log/photo.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    if len(sys.argv) > 1:
        isbn_image_dict = ast.literal_eval(sys.argv[1])
        if isinstance(isbn_image_dict, dict):
            target_sizes = [(120,83), (520,322), (300,186), (289,184), (468,290)]
            output_folder = "/home/cover"
            for isbn, image_url in isbn_image_dict.items():
                for target_size in target_sizes:
                    scale_and_save_image(image_url, target_size, output_folder)
        else:
            logging.error("Некоретные данные")
    else:
        logging.error("Не передан json")

        
