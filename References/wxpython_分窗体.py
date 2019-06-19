import wx
import wx.lib.agw.customtreectrl as CT


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title, pos, size):
        # 初始化父类
        super().__init__(parent, id, title, pos, size)
        # 添加菜单栏及菜单
        self.menuBar = wx.MenuBar()
        self.file1 = wx.Menu()
        self.file2 = wx.Menu()
        # 添加菜单到菜单栏
        self.menuBar.Append(self.file1, "File")
        self.menuBar.Append(self.file2, "关于")
        # （id， 菜单项名称， 状态栏说明）  id=-1表示取一个新的id
        self.menu1 = self.file1.Append(-1, "树1", "树1...")
        self.menu2 = self.file1.Append(-1, "树2", "树2...")
        self.menu3 = self.file1.Append(-1, "树3", "树3...")
        # 显示菜单栏
        self.SetMenuBar(self.menuBar)
        # 显示状态栏(位置在框架最下方)
        self.status_bar = self.CreateStatusBar()
        # 创建分割窗，定义左右两个面板
        self.splitter = wx.SplitterWindow(self, -1)
        self.left_panel = wx.Panel(self.splitter)
        self.right_panel = wx.Panel(self.splitter)
        self.splitter.SplitVertically(self.left_panel, self.right_panel, 240)
        # 定义右面板白色背景色
        self.right_panel.SetBackgroundColour("white")
        # 创建3个树形控件
        self.tree1 = self.create_tree("tree_1", 7)
        self.tree2 = self.create_tree("tree_2", 5)
        self.tree3 = self.create_tree("tree_3", 12)
        # 将3个树形控件都放在左面板上，并用BoxSizer管理
        self.panel(self.tree1)
        self.panel(self.tree2)
        self.panel(self.tree3)
        # 初始隐藏3个树形控件
        # self.tree1.Hide()
        self.tree2.Hide()
        self.tree3.Hide()
        # 为三个菜单项绑定事件
        self.Bind(wx.EVT_MENU, self.OnMenu1, self.menu1)
        self.Bind(wx.EVT_MENU, self.OnMenu2, self.menu2)
        self.Bind(wx.EVT_MENU, self.OnMenu3, self.menu3)

    # 菜单触发的动作
    def OnMenu1(self, event):
        self.tree2.Hide()
        self.tree3.Hide()
        self.tree1.Show()

    def OnMenu2(self, event):
        self.tree1.Hide()
        self.tree3.Hide()
        self.tree2.Show()

    def OnMenu3(self, event):
        self.tree1.Hide()
        self.tree2.Hide()
        self.tree3.Show()

    def create_tree(self, name, num):
        custom_tree = CT.CustomTreeCtrl(parent=self.left_panel, pos=(0, 0), size=(240, 400),
                                        agwStyle=wx.TR_DEFAULT_STYLE)
        # 树形控件根（ct_type=1显示复选框）
        root = custom_tree.AddRoot(name, ct_type=1)
        custom_tree.CheckItem(root)
        # 定义图标
        il = wx.ImageList(16, 16)
        fldridx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16)))
        fileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16)))
        custom_tree.SetImageList(il)
        # 给根项添加图标
        custom_tree.SetItemImage(root, fldridx, wx.TreeItemIcon_Normal)
        # 创建子项
        for i in range(0, num):
            mid_name = "item_" + str(i)
            item = custom_tree.AppendItem(root, mid_name, ct_type=1)
            custom_tree.SetItemImage(item, fldridx, wx.TreeItemIcon_Normal)
            for j in range(0, 3):
                sub_name = "sub_file_" + str(j)
                sub_item = custom_tree.AppendItem(item, sub_name, ct_type=1)
                custom_tree.SetItemImage(sub_item, fileidx, wx.TreeItemIcon_Normal)
        # 展开根项
        custom_tree.Expand(root)
        return custom_tree

    def panel(self, control):
        vbox_left = wx.BoxSizer(wx.VERTICAL)
        self.left_panel.SetSizer(vbox_left)
        vbox_left.Add(control, 1, flag=wx.EXPAND | wx.ALL, border=5)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(parent=None, id=-1, title="test", pos=(600, 200), size=(600, 480))
    frame.Show()
    app.MainLoop()
