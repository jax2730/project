import cv2
import wx
from mediapipe_reshape import pre_image, get_pos
from ultralytics import YOLO



class mediapipeApp(wx.App):
    def __init__(self):
        wx.App.__init__(self)
        self.frame = wx.Frame(None, title="Mediapipe_UI")
        self.panel = wx.Panel(self.frame)
        # 修改为实例变量
        self.VERTICAL = wx.BoxSizer(wx.VERTICAL)  # 改为self.VERTICAL
        self.HORIZONTAL = wx.BoxSizer(wx.HORIZONTAL)  # 改为self.HORIZONTAL
        
        image = wx.Image(500,500)
        self.image = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(image))
        self.opare = wx.StaticBoxSizer(wx.StaticBox(self.panel, wx.ID_ANY, "操作栏"),
                                       wx.VERTICAL)
        # 图片操作栏
        self.image_op = wx.StaticBoxSizer(wx.StaticBox(self.opare.GetStaticBox(), wx.ID_ANY, "图片操作栏"),
                                       wx.VERTICAL)
        grider = wx.GridSizer(0, 2, 0, 9)
        btn_open = wx.Button(self.image_op.GetStaticBox(), label="打开文件")
        btn_points = wx.Button(self.image_op.GetStaticBox(), label="检测关键点")
        btn_pose = wx.Button(self.image_op.GetStaticBox(), label="检测姿态")
        # 状态栏，文本输入框
        self.sympol = wx.StaticBoxSizer(wx.StaticBox(self.opare.GetStaticBox(), wx.ID_ANY, "状态栏"),
                                          wx.HORIZONTAL)
        self.text_ctrl = wx.TextCtrl(self.sympol.GetStaticBox(), size=(200,300))

        # -----------------------------------
        #   设置控件 ： 按钮、文本输入框等
        # -----------------------------------
        btn_open.Bind(wx.EVT_BUTTON, self.openfile)
        btn_points.Bind(wx.EVT_BUTTON, self.points)
        btn_pose.Bind(wx.EVT_BUTTON, self.pose_detection)  # 新增这行
        # ------------------------------------
        # 控件分布
        # ------------------------------------
        grider.Add(btn_open, 0, wx.ALL|wx.EXPAND, 5)
        grider.Add(btn_points, 0, wx.ALL|wx.EXPAND, 5)
        grider.Add(btn_pose, 0, wx.ALL|wx.EXPAND, 5)
        self.opare.Add(self.image_op, 0, wx.ALL|wx.EXPAND, 5)
        self.opare.Add(self.sympol, 0, wx.ALL|wx.EXPAND, 5)
        self.image_op.Add(grider, 0, wx.ALL|wx.EXPAND, 5)
        self.sympol.Add(self.text_ctrl, 0, wx.ALL|wx.EXPAND, 5)
        # 修改引用方式
        self.HORIZONTAL.Add(self.image, 0, wx.ALL|wx.EXPAND, 5)
        self.HORIZONTAL.Add(self.opare, 0, wx.ALL|wx.EXPAND, 5)
        self.VERTICAL.Add(self.HORIZONTAL)
        # ------------------------------------
        # 最终设置
        # ------------------------------------
        self.panel.SetSizer(self.VERTICAL)  # 修改为self.VERTICAL
        self.panel.Layout()
        self.HORIZONTAL.Fit(self.frame)  # 修改为self.HORIZONTAL
        self.frame.Show()
        self.PhotoMaxSize = 500
        self.filepath = ""
    def points(self, event):
        if self.filepath == "":
            struction = "错误，请先导入原始图片"
            self.text_ctrl.SetValue(struction)
            self.text_ctrl.GetValue()
        else:
            # 返回的image是cv2格式
            image = pre_image(self.filepath)
            image = cv2.resize(image, (500,500))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pic = wx.Bitmap.FromBuffer(image.shape[1], image.shape[0], image)
            self.image.SetBitmap(pic)
            self.panel.Refresh()


    def openfile(self, event):
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "choose a file",
                               wildcard=wildcard,
                               style=wx.FD_CHANGE_DIR)
        if dialog.ShowModal() == wx.ID_OK:
            self.text_ctrl.SetValue(dialog.GetPath())
        dialog.Destroy()
        self.onView()
    def onView(self):
        self.filepath = self.text_ctrl.GetValue()
        self.showImage(self.filepath)
    def showImage(self, filepath):
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        W = img.GetWidth()
        H = img.GetHeight()
        # 修复浮点数转整数警告
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = int(self.PhotoMaxSize * H / W)  # 添加int转换
        else:
            NewH = self.PhotoMaxSize
            NewW = int(self.PhotoMaxSize * W / H)  # 添加int转换
        self.W = NewW
        self.H = NewH
        img = img.Scale(NewW, NewH)
        # 替换弃用的BitmapFromImage
        self.image.SetBitmap(wx.Bitmap(img))  # 替换wx.BitmapFromImage
        self.panel.Refresh()

    def pose_detection(self, event):
        if self.filepath == "":
            struction = "错误，请先导入原始图片"
            self.text_ctrl.SetValue(struction)
        else:
            # 使用YOLO进行姿态检测
            # 确保 from ultralytics import YOLO 在文件顶部已导入
            # 确保 import cv2 在文件顶部已导入

            # 加载YOLO姿态模型
            # 模型文件 'yolo11n-pose.pt' 应位于 mediapipe-master 文件夹的根目录
            model_path = 'yolo11n-pose.pt' 
            try:
                # 检查 self 是否已经有 model 实例，避免重复加载
                if not hasattr(self, 'yolo_model') or self.yolo_model is None:
                    self.yolo_model = YOLO(model_path)
                model = self.yolo_model
            except Exception as e:
                self.text_ctrl.SetValue(f"错误：无法加载YOLO模型 {model_path}. {e}")
                return

            # 读取图片
            image_bgr = cv2.imread(self.filepath) # YOLO通常处理BGR图像
            if image_bgr is None:
                self.text_ctrl.SetValue(f"错误：无法读取图片 {self.filepath}")
                return
            
            # 执行推理
            try:
                results = model(image_bgr, verbose=False) # results is a list of Results objects, verbose=False to reduce console output
            except Exception as e:
                self.text_ctrl.SetValue(f"错误：YOLO推理失败. {e}")
                return

            # 绘制结果
            annotated_image = image_bgr.copy() # Start with a copy of the original BGR image

            if results and len(results) > 0 and results[0].keypoints is not None and results[0].keypoints.xy.numel() > 0:
                # results[0].plot() 返回一个带标注的NumPy数组 (BGR格式)
                annotated_image = results[0].plot(boxes=False) # plot only keypoints, not bounding boxes
                
                # 可以在这里添加自定义的文本或姿态判断逻辑
                # 例如，获取关键点数据:
                # keypoints_data_normalized = results[0].keypoints.xyn[0].cpu().numpy() # 第一个人, 归一化坐标 (x,y)
                # keypoints_data_pixels = results[0].keypoints.xy[0].cpu().numpy() # 第一个人, 像素坐标 (x,y)
                # confidences = results[0].keypoints.conf[0].cpu().numpy() # 置信度

                # 示例：简单地在图像上显示检测到的姿态数量
                num_poses = len(results[0].keypoints.xy)
                cv2.putText(annotated_image, f"Poses: {num_poses} (YOLO)", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            else:
                # 没有检测到姿态，显示提示信息
                cv2.putText(annotated_image, "No pose detected (YOLO)", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # 显示结果
            annotated_image_resized = cv2.resize(annotated_image, (500,500))
            # annotated_image_resized 已经是BGR格式
            # wx.Bitmap.FromBuffer expects RGB or RGBA data. OpenCV images are BGR.
            annotated_image_rgb = cv2.cvtColor(annotated_image_resized, cv2.COLOR_BGR2RGB)
            pic = wx.Bitmap.FromBuffer(annotated_image_rgb.shape[1], annotated_image_rgb.shape[0], annotated_image_rgb.tobytes())
            self.image.SetBitmap(pic)
            self.panel.Refresh()

if __name__ == '__main__':
    app = mediapipeApp()
    app.MainLoop()