# WebCam

USB Video Class (UVC) 是 USB 设备类规范，定义了视频流设备无需额外驱动即可通过标准 USB 接口传输未压缩或压缩视频数据的通信协议。Linux通过 Video for Linux 2 (V4L2) 子系统将其抽象为 /dev/videoX 设备节点，并提供标准 ioctl 接口 (如查询格式、设置帧率、申请缓冲区) 和内存映射 (mmap) 或用户指针方式获取视频帧。
