import sys
import wx
import os
import glob

#Method to clean up lines
def methStrip(strTag, strLine):
    strClean = strLine.replace("<", "")
    strClean = strClean.replace(">", "")
    strClean = strClean.replace(strTag, "")
    strClean = strClean.replace("\n", "")
    strClean = strClean.replace("/", "")
    return strClean
    
class ConvertMXML(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(250, 300))



        
        
        
        # Panel to put controls on, probably not necessary
        panel = wx.Panel(self)
                # and a few controls
        text = wx.StaticText(panel, -1, "MXML Dir:")
        text.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        text.SetSize(text.GetBestSize())
        btnBrowseInput = wx.Button(panel, -1, "Browse")
        lblOutput= wx.StaticText(panel, -1, "Output Dir:")
        btnBrowseOutput = wx.Button(panel, -1, "Browse")
        btnConvert = wx.Button(panel, -1, "Convert")
        txtInput = wx.TextCtrl(panel, -1, "", size=(300, -1))
        txtOutput = wx.TextCtrl(panel, -1, "", size=(300, -1))

        # bind the button events to handlers
        self.Bind(wx.EVT_BUTTON, self.OnBrowseInputClick, btnBrowseInput)
        self.Bind(wx.EVT_BUTTON, self.OnBrowseOutputClick, btnBrowseOutput)
        self.Bind(wx.EVT_BUTTON, self.OnConvertClick, btnConvert)


        
        #TOP ROW
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 0, wx.ALL, 5)
        sizer.Add(txtInput, 0, wx.ALL, 5)
        sizer.Add(btnBrowseInput, 0, wx.ALL, 5)
        #Second Row
        
        sizer.Add(lblOutput, 0, wx.ALL, 5)
        sizer.Add(txtOutput, 0, wx.ALL, 5)
        sizer.Add(btnBrowseOutput, 0, wx.ALL, 5)
        sizer.Add(btnConvert, 5, wx.ALL, 5)

        #bind controls or some shit
        self.txtInput = txtInput
        self.txtOutput = txtOutput
        
        panel.SetSizer(sizer)
        panel.Layout()


    def OnBrowseInputClick(self, evt):
        
        dlgInput = wx.DirDialog(self, "Choose the Input Directory", style = wx.DD_DEFAULT_STYLE)
        dlgInput.ShowModal()
        self.txtInput.Clear()
        self.txtInput.WriteText(dlgInput.GetPath())
        

    def OnBrowseOutputClick(self, evt):
        
        dlgOutput = wx.DirDialog(self, "Choose the Output Directory", style = wx.DD_DEFAULT_STYLE)
        dlgOutput.ShowModal()
        self.txtInput.Clear() 
        self.txtOutput.WriteText(dlgOutput.GetPath())

        

        
    def OnConvertClick(self, evt):
        
        strPath = os.path.join(self.txtInput.GetLineText(0),"*.xml")
        #Unique ID for this song
        iID = 0
        #iPosition that isn't really used
        iPosition = 0;
        #note duration in numbers
        iDuration = 0;
        for name in glob.glob(strPath):
            #for some reason it uses the input path instead of the one i explicitly assign
            #probably just using the 'current dir' or something.
            filedir = r"D:\\output\\"
            output_file = open(os.path.join(filedir, name.replace(".xml", ".txt")), "w")
            #os.path.join(self.txtOutput.GetLineText(0)
            print "Converting " + name
            #convert stuff here
            fileToConvert = open(name, "r")
            while True:
                line = fileToConvert.readline()
                if not line: break
                if line[:8] == "<part id":
                    
                    #define array which will end up being the line we will be writing
                    strArrNewLine = ["0"]*10
                    #Put text file name i guess?
                    strArrNewLine[9] = os.path.basename(name)
                    strArrNewLine[9] = strArrNewLine[9].replace(".xml", "")
                    #send to cleanup function to get rid of text we don't want
                    strPartId = methStrip("part id=", line)                    
                    strArrNewLine[8] = strPartId
                    #define long duration, this is used for note placement
                    iLongDuration = 0;
                    #/part is the end of this instrument/track
                    last_pos = fileToConvert.tell()
                    #iDuration is declared up here as zero becuase i want to i guess
                    iDuration =0
                    while fileToConvert.readline() != "</part>":
                        
                        
                        line = fileToConvert.readline()
                          
                        if not line: break
                        
                        #If <note> tag then start to create the array we will log.
                        #It will go until it finds the </note> tag
                        if line[:6] == "<note>":
                            
                            #declare and assign variables that will be used for this set of note tags

                            strArrNewLine[0] = iID
                            strArrNewLine[1] = iPosition
                            fileToConvert.seek(last_pos)
                            while line != "</note>":
                                #OK, so we should have all of the fields filled out,
                                #time to write them to a file
                                #It feels like this should be at the end but I was having problems with it there
                                if line[:7] == "</note>":
                                    iPosition = iPosition +1
                                    iID = iID + 1
                                    strArrNewLine[0] = iID
                                    strArrNewLine[1] = iPosition
                                    output_file.write(", ".join(map(str, strArrNewLine)))
                                    output_file.write("\n")
                                    
                                    
                                line = fileToConvert.readline()
                                if not line: break
                                if line[:6] == "<step>":
                                    strArrNewLine[2] = methStrip("step", line)
                                    
                                elif line[:8] == "<octave>":
                                    strArrNewLine[3] = methStrip("octave", line)
                                elif line[:10] == "<duration>":
                                    iDuration = methStrip("duration", line);
                                    strArrNewLine[4] = iDuration
                                    iLongDuration = int(iLongDuration) + int(iDuration)
                                    strArrNewLine[5] = iLongDuration
                                elif line[:6] == "<type>":
                                    strArrNewLine[6] = methStrip("type", line)
                                elif line[:6] == "<mode>":
                                    strArrNewLine[7] = methStrip("mode", line)

                                    #If it's a rest, the note = 9 and oactiave = 999
                                elif line[:5] == "<rest":
                                    strArrNewLine[2] = "R"
                                    strArrNewLine[3] = "999"
                                elif line[:8] == "<part id":
                                    strArrNewLine[8] = methStrip("part id=", line)
                                    #reset long duration since it's a new part
                                    iLongDuration =0
                                    
                                    #If the <chord /> tag is present, we want to
                                    #rollback the iLongDuration as the note is being
                                    #played at the same time as the last note
                                elif line[:6] == "<chord":
                                        iLongDuration = int(iLongDuration) - int(iDuration)
                                        strArrNewLine[5] =iLongDuration
        
            fileToConvert.close()
            output_file.close()
         
        

        
        

class MyApp(wx.App):
    def OnInit(self):
        frame = ConvertMXML(None, "Convert MusicXML")
        self.SetTopWindow(frame)

        

        frame.Show(True)
        return True

        
app = MyApp(redirect=True)
app.MainLoop()

