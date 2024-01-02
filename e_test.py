import requests
import time

# 要测试的服务器的URL
server_url = 'http://192.168.0.94:5000/forward/介绍一下云南的小吃'

# 定义要发送多少次请求进行测试
num_requests = 100

# 记录每次请求的响应时间
response_times = []

for i in range(num_requests):
    start_time = time.time()
    response = requests.get(server_url)
    end_time = time.time()

    duration = end_time - start_time
    response_times.append(duration)

    # 打印响应内容
    if response.status_code == 200:
        print(f'Request {i + 1}/{num_requests}: {response.status_code} in {duration:.4f} seconds, Response: {response.text}')
    else:
        print(f'Request {i + 1}/{num_requests}: Error {response.status_code} in {duration:.4f} seconds')

# 计算并显示结果
average_time = sum(response_times) / len(response_times)
max_time = max(response_times)
min_time = min(response_times)
print(f'\nAverage response time: {average_time:.4f} seconds')
print(f'Max response time: {max_time:.4f} seconds')
print(f'Min response time: {min_time:.4f} seconds')