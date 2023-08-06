# -- coding: utf-8 --
# @Time : 2021/12/8
# @Author : ykk648
# @Project : https://github.com/ykk648/AI_power
from cv_queue import CVQueue
from cv_image import CVImage

get_q = CVQueue(10, mem_name='okbb')
# get_buf =
while True:
    get_buf, get_buffer_len = get_q.get()
    image_to_show = bytes(get_buf.buf[:get_buffer_len])
    get_q.get_ok()
    # self.cv_image = np.frombuffer(get_buf, np.uint8).reshape((1080, 1920, 3))
    ttt = CVImage(image_to_show, image_format='bytes').show()
    # ttt.reshape((1080, 1920, 3).show()