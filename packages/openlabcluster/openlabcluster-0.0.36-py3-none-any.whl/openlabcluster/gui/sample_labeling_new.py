
import matplotlib.font_manager as font_manager
import os
import traceback
import wx
import wx.lib.scrolledpanel
from wx.lib.agw.pygauge import PyGauge

import openlabcluster
from openlabcluster.training_utils.ssl.data_loader import get_data_list
from openlabcluster.utils import auxiliaryfunctions
from wx.lib.pubsub import pub
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
media_path = os.path.join(openlabcluster.__path__[0], "gui", "media")

selection_method_options = ["Marginal Index (MI)","Core Set (CS)", "Cluster Center (Top)",
                            "Cluster Random (Rand)", "Uniform (Uni)", ]

# class Sample_labeling(wx.Panel):
class Sample_labeling(wx.lib.scrolledpanel.ScrolledPanel):
    """
    """

    def __init__(self, parent, gui_size, cfg, statusBar):
        """Constructor"""
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent=parent)
        self.progress = 0
        self.method = "automatic"
        self.config = cfg
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.parent = parent
        text = wx.StaticText(self, label="OpenLabCluster - Step 3. Behavior Classification Map with Active Learning")
        self.sizer.Add(text,0, flag=wx.EXPAND| wx.TOP | wx.LEFT | wx.BOTTOM, border=15)

        line1 = wx.StaticLine(self)
        self.sizer.Add(
            line1,0, flag=wx.EXPAND |wx.TOP| wx.BOTTOM, border=5
        )
        self.statusBar = statusBar
        # select model
        sb = wx.StaticBox(self, label="")
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL) # selection and plot parameter
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL) # used for metrics 
        self.hbox5 = wx.BoxSizer(wx.HORIZONTAL) # gauge
        self.hbox6 = wx.BoxSizer(wx.HORIZONTAL) # training parameter
        self.config_file = auxiliaryfunctions.read_config(self.config)

        select_text = wx.StaticBox(self, label="Active Learning Method")
        selectboxsizer = wx.StaticBoxSizer(select_text, wx.VERTICAL)
        self.select_choice = wx.ComboBox(self, style=wx.CB_READONLY)
        self.select_choice.Set(selection_method_options)
        self.select_choice.SetValue(self.config_file['sample_method'])
        self.select_choice.Bind(wx.EVT_COMBOBOX, self.nextSelection)
        selectboxsizer.Add(self.select_choice, 10, wx.EXPAND | wx.TOP | wx.BOTTOM, 2)
        self.hbox1.Add(selectboxsizer, 10, wx.EXPAND | wx.TOP | wx.BOTTOM, 2)

        trainingindex_box = wx.StaticBox(self, label="# Samples per Selection")
        trainingindex_boxsizer = wx.StaticBoxSizer(trainingindex_box, wx.VERTICAL)
        self.trainingindex = wx.SpinCtrl(self, value=str(self.config_file.get('label_budget', 10)), min=1)
        trainingindex_boxsizer.Add(self.trainingindex, 10, wx.EXPAND | wx.TOP | wx.BOTTOM, 2)
        self.hbox1.Add(trainingindex_boxsizer, 10, wx.EXPAND | wx.TOP | wx.BOTTOM|wx.RIGHT, 2)

        epoch_box = wx.StaticBox(self, label="Maximum Epochs")
        epoch_boxizer = wx.StaticBoxSizer(epoch_box, wx.VERTICAL)
        self.epoch = wx.SpinCtrl(self, value="10", min=1)
        epoch_boxizer.Add(self.epoch, 10, wx.EXPAND | wx.TOP | wx.BOTTOM, 2)
        self.hbox1.Add(epoch_boxizer, 10, wx.EXPAND | wx.TOP | wx.BOTTOM|wx.RIGHT, 2)

        dim_text = wx.StaticBox(self, label="Cluster Map Dimension")
        dimboxsizer = wx.StaticBoxSizer(dim_text, wx.VERTICAL)
        self.dim_choice = wx.ComboBox(self, style=wx.CB_READONLY)
        self.dim_choice.Bind(wx.EVT_COMBOBOX, self.update_image_panel)
        options = ["2d", "3d"]
        self.dim_choice.Set(options)
        self.dim_choice.SetValue("2d")
        dimboxsizer.Add(self.dim_choice, 10, wx.EXPAND | wx.TOP | wx.BOTTOM, 2)
        self.hbox1.Add(dimboxsizer, 10, wx.EXPAND | wx.TOP | wx.BOTTOM|wx.RIGHT, 2)

        reducer_text = wx.StaticBox(self, label="Dimension Reduction Method")
        reducerboxsizer = wx.StaticBoxSizer(reducer_text, wx.VERTICAL)
        self.reducer_choice = wx.ComboBox(self, style=wx.CB_READONLY)
        self.reducer_choice.Bind(wx.EVT_COMBOBOX, self.update_image_panel)
        reducer_options = ["PCA", "tSNE", "UMAP"]
        self.reducer_choice.Set(reducer_options)
        self.reducer_choice.SetValue("PCA")
        reducerboxsizer.Add(self.reducer_choice, 10, wx.EXPAND | wx.TOP | wx.BOTTOM, 2)
        self.hbox1.Add(reducerboxsizer, 10, wx.EXPAND | wx.TOP | wx.BOTTOM|wx.RIGHT, 2)

        self.sizer.Add(
            self.hbox1,
            0,
            flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,
            border=10,
        )

        self.metrics_box = wx.BoxSizer(wx.HORIZONTAL)
        
        font = wx.Font(25, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL)

        labelled_points = wx.StaticText(self, label=" points labelled")
        labelled_points_num = wx.StaticText(self, label="0")
        labelled_points_num.SetFont(font)

        unlabelled_points = wx.StaticText(self, label=" points unlabelled")
        unlabelled_points_num = wx.StaticText(self, label="0")
        unlabelled_points_num.SetFont(font)

        self.cal_har_index = wx.StaticText(self, label=" Calinski-Harabasz Index")
        self.cal_har_index_num = wx.StaticText(self, label="0")
        self.cal_har_index_num.SetFont(font)

        self.dav_bould_index = wx.StaticText(self, label=" Davies-Bouldin Index")
        self.dav_bould_index_num = wx.StaticText(self, label="0")
        self.dav_bould_index_num.SetFont(font)

        self.train_acc = wx.StaticText(self, label=" Training Accuracy")
        self.train_acc_num = wx.StaticText(self, label="0.00")
        self.train_acc_num.SetFont(font)

        self.metrics_box.Add(labelled_points_num,   flag=wx.TOP | wx.LEFT | wx.EXPAND, border=15)
        self.metrics_box.Add(labelled_points,       flag=wx.TOP | wx.EXPAND, border=15)
        self.metrics_box.Add(unlabelled_points_num, flag=wx.TOP | wx.LEFT | wx.EXPAND, border=15)
        self.metrics_box.Add(unlabelled_points,     flag=wx.TOP | wx.EXPAND, border=15)
        self.metrics_box.Add(self.cal_har_index_num,     flag=wx.TOP | wx.LEFT | wx.EXPAND, border=15)
        self.metrics_box.Add(self.cal_har_index,         flag=wx.TOP | wx.EXPAND, border=15)
        self.metrics_box.Add(self.dav_bould_index_num,   flag=wx.TOP | wx.LEFT | wx.EXPAND, border=15)
        self.metrics_box.Add(self.dav_bould_index,       flag=wx.TOP | wx.EXPAND, border=15)
        self.metrics_box.Add(self.train_acc_num, flag=wx.TOP | wx.EXPAND, border=15)
        self.metrics_box.Add(self.train_acc,  flag=wx.TOP | wx.EXPAND, border=15 )
        self.sizer.Add(self.metrics_box,0, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,
            border=10)


        self.help_button = wx.Button(self, label="Help")
        self.help_button.Bind(wx.EVT_BUTTON, self.help_function)

        self.evaluation_button = wx.Button(self, label="Get Results")
        self.evaluation_button.Bind(wx.EVT_BUTTON, self.evaluation_function)

        from openlabcluster.gui.labeling_toolbox_ic import PlotGUI_panel
        from openlabcluster.gui.media.label_video import Labeling_panel
        displays = (
            wx.Display(i) for i in range(wx.Display.GetCount())
        )  # Gets the number of displays
        screenSizes = [
            display.GetGeometry().GetSize() for display in displays
        ]  # Gets the size of each display
        index = 0  # For display 1.
        screenWidth = screenSizes[index][0]
        screenHeight = screenSizes[index][1]
        self.gui_size = (screenWidth * 0.7, screenHeight * 0.85)

        #sb = wx.StaticBox(self, label="Interative Action Recognition")
        self.oper_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.oper_2 = wx.BoxSizer(wx.HORIZONTAL)
        # modeltype is essentially based on value in config (one of "seq2seq", "semi_seq2seq"). It needs to be "semi_seq2seq to get class values"
        self.image_panel = PlotGUI_panel(self, self.config, self.select_choice.GetValue(), self.trainingindex.GetValue())
        self.video_panel = None
        
        def current_sample_wrapper(*args, **kwargs):
            self.image_panel.current_sample(*args, **kwargs)
            self.metrics_box.Layout()
            self.sizer.Layout()
            self.Layout()
            # self.parent.Layout()

        def label_points_wrapper():
            labelled_points_num.SetLabelText(str(self.video_panel.total_labelled))
            unlabelled_points_num.SetLabelText(
                str(self.image_panel.extracted.dataset_size_train - self.video_panel.total_labelled))


        self.video_panel = Labeling_panel(self, self.config, current_sample_wrapper, label_points_wrapper,
                                          self.image_panel.update_labeled, self.image_panel.get_suggest) # every time click load video will reload the configure file
        self.image_panel.initialize_video_coonection(self.video_panel.load_video)
        labelled_points_num.SetLabelText(str(self.video_panel.total_labelled))
        unlabelled_points_num.SetLabelText(str(self.image_panel.extracted.dataset_size_train - self.video_panel.total_labelled))

        self.oper_1.Add(self.image_panel,15, wx.EXPAND | wx.TOP | wx.BOTTOM|wx.RIGHT, 1)
        self.oper_1.Add(self.video_panel, 15, wx.EXPAND | wx.TOP | wx.BOTTOM|wx.RIGHT|wx.LEFT,1)

        self.gauge = wx.Gauge(self, wx.ID_ANY, self.config_file['su_epoch'], size=(-1, 25)) # width height
        # self.gauge = PyGauge(self, wx.ID_ANY, self.config_file['su_epoch'], size=(-1, 25)) # width height
        # self.gauge.SetBarColour(wx.Colour(30, 117, 251))
        self.hbox5.Add(self.gauge, 1,  wx.EXPAND | wx.TOP | wx.BOTTOM,)
        self.retrain = wx.Button(self, label='Run Classification')
        self.retrain.Bind(wx.EVT_BUTTON, self.retrain_network)

        # , wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)

        self.stop = wx.Button(self, label="Stop Classification")
        self.stop.Bind(wx.EVT_BUTTON, self.stop_train)

        self.next_selection = wx.Button(self, label='Next Selection')
        self.next_selection.Bind(wx.EVT_BUTTON, self.nextSelection)



        self.oper_2.Add(self.retrain,        1,   flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)
        self.oper_2.Add(self.stop,            1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)
        self.oper_2.Add(self.next_selection,   1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)
        # self.oper_2.Add(self.reset,            1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)
        self.oper_2.Add(self.help_button,       1,flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)
        self.oper_2.Add(self.evaluation_button, 1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)

        self.sizer.Add(self.hbox5,0, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,
            border=10)
        self.sizer.Add(self.oper_2,0, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,
            border=10)
        self.sizer.Add(self.oper_1, 0, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,
            border=10)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

        self.image_panel.savelabel(None) # load videos

        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
        self.Layout()

        self.SetupScrolling()

    def on_focus(self, event):
        pass

    def help_function(self, event):
        help_text = """
        Behavior Classification Map
        Set the Training Parameters
        1. Selection Method: In this part, your selection will decide which method GUI uses to select samples for annotation. there are four possible choices ("Marginal Index (MI)", "Core Set (CS)", "Cluster Center (TOP)", "Cluster Random (Rand)", "Uniform").
        2. \# Samples per Selection: the number of samples you want to label in the current selection stage. You can select or deselect samples in the behavior classification map.
        3. Maximum Epochs: the maximum epoch the network will be trained when performing the action recognition.
        4. Cluster Map Dimension: you can choose "2d" or "3d" if it is "2d" the Cluster Map will be shown in 2D dimension, otherwise it is 3D dimension.
        5. Dimension Reduction Method: possible choices are "PCA", "tSNE", "UMAP". The GUI will use the chosen reduction method to perform dimension reduction and show results in Cluster Map.
        
        Buttons:
            
            i Run Classification: save annotation results and train the action recognition model.
            ii Stop Classification: stop training.
            iv  Next Selection: suggest a new set of samples based on with indicated active learning method. **Notice**: if you change Cluster Map Dimension or Dimension Reduction Method, click the **Next Selection** to show suggested samples.
            vi Get Results: get the Behavior Classification Map (predicted class label) from the trained model on unlabeled samples.        
        
        Plots
            1. Behavior Classification Plot:
                **Visualization mode**: The points representing each action segment is shown in black for visualization, it can be visualized in 2D or 3D with different dimension reduction method.
                **Annotation mode**: In the mode, dots for each action segment in a different color in the Behavior Classification plot (only in 2D).
                    Red: current sample for annotating and the video segment is shown on the right. 
                    Blue: the suggested samples for annotating in this iteration (deselect them by clicking the point).
                    Green: samples have been annotated.
            
                Buttons:
                  * Zoom: zoom in or zoom out the plot.
                  * Pan: move the plot around.
            
            2. Videos Panel:
                Left panel: The corresponding video of the action segment which is shown in the Behavior Classification Map in red.
                Right panel: The class name and class id. According to the video, one can label the action segment.
                Buttons:
                  * Previous: load the previous video.
                  * Play: play the video.
                  * Next: go to the next video. 
        """
        wx.MessageBox(help_text, "Help", wx.OK | wx.ICON_INFORMATION)

    def evaluation_function(self, event):
        '''
        Create excel file with results from running model on data 
        '''
        self.image_panel.extract_hiddenstate()
        labels = self.image_panel.extracted.pred_label
        transformed = self.image_panel.extracted.transformed
        import pandas as pd
        import yaml

        f = open(self.config, 'r')
        config = yaml.safe_load(f)

        _, _, names = get_data_list([os.path.join(config['data_path'], config['train'])], return_video=True, videos_exist=True)
        names = [name.decode('UTF-8') for name in names]

        print(len(names), names)
        print(len(labels), labels)

        label_names = [config['class_name'][int(i)-1] for i in labels]

        df = pd.DataFrame({'video_names': names, 'labels': labels, 'label_names': label_names})

        df.to_excel(os.path.join(config['output_path'], 'output.xlsx'))
        save_dir = os.path.join(config['output_path'], 'behavior_classification_map.jpg')
        self.plot_behavior_map(config['num_class'], config['class_name'], transformed, labels, save_dir)

    def select_config(self, event):
        """
        """
        self.config = self.sel_config.GetPath()

    def select_trml(self, event):
        """
        """
        if self.sel_trml.IsShown():
            self.trml = self.sel_trml.GetPath()
            if self.trml == "":
                wx.MessageBox(
                    "Please choose the trained model to load the project",
                    "Error",
                    wx.OK | wx.ICON_ERROR,
                )
                self.loaded = False

    def chooseOption(self, event):
        if self.model_comparison_choice.GetStringSelection() == "Yes":
            self.network_box.Show()
            self.networks_to_compare.Show()
            self.augmentation_box.Show()
            self.augmentation_to_compare.Show()
            self.shuffles_text.Show()
            self.shuffles.Show()
            self.net_choice.Enable(False)
            self.select_choice.Enable(False)
            self.shuffle.Enable(False)
            self.SetSizer(self.sizer)
            self.sizer.Fit(self)
            self.get_network_names(event)
            self.get_augmentation_method_names(event)
        else:
            self.net_choice.Enable(True)
            self.select_choice.Enable(True)
            self.shuffle.Enable(True)
            self.shuffles_text.Hide()
            self.shuffles.Hide()
            self.network_box.Hide()
            self.networks_to_compare.Hide()
            self.augmentation_box.Hide()
            self.augmentation_to_compare.Hide()
            self.SetSizer(self.sizer)
            self.sizer.Fit(self)

    def get_network_names(self, event):
        self.net_type = list(self.networks_to_compare.GetCheckedStrings())

    def get_augmentation_method_names(self, event):
        self.aug_type = list(self.augmentation_to_compare.GetCheckedStrings())

    def selecting_samples(self, event):
        """
        """
        from openlabcluster.gui.labeling_toolbox_ic import show

        show(self.config, self.trml, self.net_choice.GetValue(), self.select_choice.GetValue(), self.trainingindex.GetValue())

    def labeling_video(self, event):
        from openlabcluster.gui.media.label_video import show
        if self.sel_labelpath.GetPath():
            show(self.config, self.sel_labelpath.GetPath())
        else:
            config_file = auxiliaryfunctions.read_config(self.config)
            show(self.config, config_file['selected_path'])

    def draw_plot(self):
        self.work.plot()

    def retrain_network(self, event):
        self.image_panel.deactive_display()
        try:
            self.video_panel.sample
            self.video_panel.savelabel()
        except:
            pass
        pub.subscribe(self.updateProgress, "update")
        pub.subscribe(self.on_finish, "finish_iter")
        pub.subscribe(self.draw_plot, "plot_iter")
        from openlabcluster.training_utils.itertrain import train_network
        self.statusBar.SetStatusText('Action Recognition Started')
        #wx.MessageBox('Action Recognition Start', "Information")
        self.btn = event.GetEventObject()
        self.gauge.SetRange(self.epoch.GetValue())
        self.gauge.SetValue(0)
        self.progress = 0

        self.retrain.Enable(False)

        try:
            self.work = train_network(self.config, self.image_panel.image_panel, epochs=int(self.epoch.GetValue()), acc_text = self.train_acc_num)
            self.select_choice.Enable(False)
            self.trainingindex.Enable(False)
            self.epoch.Enable(False)
            self.dim_choice.Enable(False)
            self.reducer_choice.Enable(False)

        except Exception as e:
            print(traceback.format_exc())
            wx.MessageBox('Error while training. Look in terminal for more information', 'Training Error', wx.OK | wx.ICON_ERROR) 


    def stop_train(self, event):
        self.work.stop()
        self.select_choice.Enable(True)
        self.trainingindex.Enable(True)
        self.epoch.Enable(True)
        self.dim_choice.Enable(True)
        self.reducer_choice.Enable(True)
        self.statusBar.SetStatusText('Training Stopped')
        #wx.MessageBox('Training Stopped', 'Message')
        pub.unsubscribe(self.updateProgress, "update")
        pub.unsubscribe(self.draw_plot, "plot_iter")
        #pub.unsubscribe(self.on_finish, "finish_iter")
        self.retrain.Enable(True)
        self.statusBar.SetStatusText('')
        self.work.join()
        self.image_panel.deactive_display()

    def nextSelection(self, event):
        # save labeled sample first
        self.video_panel.savelabel()
        self.dim_choice.SetValue("2d")
        self.update_image_panel(None)
        #self.image_panel.ok.Enable(True)
        self.image_panel.active_display()
        self.image_panel.refresh(event, self.select_choice.GetValue())
        self.statusBar.SetStatusText('')

    def updateProgress(self, step):
        self.progress += step
        self.gauge.SetValue(self.progress)

        # print('gt_label', self.image_panel.extracted.gt_label)
        # print('hidarry', self.image_panel.extracted.hidarray.numpy().shape)
        # print('pred_label', self.image_panel.extracted.pred_label.numpy().shape)

        # kmeans = KMeans(n_clusters=self.video_panel.list.GetItemCount()).fit(self.image_panel.extracted.transformed) # using 2 features 
        kmeans = KMeans(n_clusters=self.video_panel.list.GetItemCount()).fit(self.image_panel.extracted.hidarray) # using entire hidden state
        # calculate scores
        labels = kmeans.labels_
        data = self.image_panel.extracted.transformed
        self.cal_har_index_num.SetLabelText(str(round(calinski_harabasz_score(data, labels ))))
        self.dav_bould_index_num.SetLabelText(str(round(davies_bouldin_score(data, labels), 2)))
        self.train_acc_num.SetLabelText(f'{self.work.acc:.2f}')
        self.metrics_box.Layout()
        self.sizer.Layout()
        self.Layout()

    def on_finish(self):
        """conversion process finished"""

        self.retrain.Enable(True)
        self.select_choice.Enable(True)
        self.trainingindex.Enable(True)
        self.epoch.Enable(True)
        self.dim_choice.Enable(True)
        self.reducer_choice.Enable(True)
        self.Close()
        self.statusBar.SetStatusText('')
        pub.unsubscribe(self.updateProgress, "update")
        pub.unsubscribe(self.on_finish, "finish_iter")

    def update_image_panel(self, event):
        dim = self.dim_choice.GetValue()
        method = self.reducer_choice.GetValue()
        self.image_panel.update_image_panel(dim, method)

    def change_model(self, event):
        self.sel_trml.Enable(True)

    def change_net(self, event):
        self.net_choice.Enable(True)

    def change_sammethod(self, event):
        self.select_choice.Enable(True)

    def change_sampath(self, event):
        self.sel_labelpath.Enable(True)

    def reset_create_training_dataset(self, event):
        """
        Reset to default
        """
        # self.config = []
        self.sel_config.SetPath("")
        # self.shuffles.SetValue("1")
        self.net_choice.SetValue("resnet_50")
        self.select_choice.SetValue("default")
        self.model_comparison_choice.SetSelection(1)
        self.network_box.Hide()
        self.networks_to_compare.Hide()
        self.augmentation_box.Hide()
        self.augmentation_to_compare.Hide()
        self.shuffles_text.Hide()
        self.shuffles.Hide()
        self.net_choice.Enable(True)
        self.select_choice.Enable(True)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
        self.Layout()

    def plot_behavior_map(self, num_classes, class_name, transformed, pred_label, save_dir):
        if isinstance(num_classes, list):
            num_classes = num_classes[0]
        cmap = plt.cm.get_cmap('hsv', num_classes)

        font = {'family': 'serif',
                'weight': 'normal',
                'size': 11,
                }
        try:
            assert len(class_name) == num_classes
        except:
            wx.MessageBox('Numer of Classes Mismatch Class Name',   "Error",
                        wx.OK | wx.ICON_ERROR)
        for i in range(num_classes):
            plt.scatter(transformed[pred_label==i+1, 0],
                        transformed[pred_label==i+1, 1],
                        label=class_name[i], c = cmap(i), s=10)
        plt.xticks(fontsize=11)
        plt.yticks(fontsize=11)
        plt.xlabel('Dimension 1', fontdict=font)
        plt.ylabel('Dimension 2', fontdict=font)
        plt.title('Behavior Classification Map', fontdict=font)
        font = font_manager.FontProperties(family='Comic Sans MS',
                                           style='normal', size=11)

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          ncol=3, prop=font)
        plt.tight_layout()
        plt.show()
        plt.savefig(save_dir)



