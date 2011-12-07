class Config:
  #defaults
  app_id       = 3743872231 
  width        = 80

  def __init__(self, section):
    self.section = section
  
  def load(self):
    file_path = os.path.expanduser('~/.pybo')
    cp = ConfigParser.ConfigParser()
    cp.read(file_path)
    if not cp.has_section(self.section):
      cp.add_section(self.section)
    
    attrs = ['username','password','app_id','width']
    #check
    self.cp_attr(cp,attrs)
    self.raw_attr(attrs[:3])
    #update
    self.update_attr(cp,attrs)
    f = open(file_path,'w')
    cp.write(f)
    f.close()

  def update_attr(self,config_parser,options):
    for attr in options:
      config_parser.set(self.section,attr,getattr(self,attr,''))

  def cp_attr(self,config_parser,options):
    for attr in options:
      if config_parser.has_option(self.section,attr):
        setattr(self,attr,config_parser.get(self.section,attr))

  def raw_attr(self,options):
    for attr in options:
      while not getattr(self,attr,None):
        setattr(self,attr,raw_input('%s : ' % attr))
  
  def __getitem__(self,key):
    if key in ('username','password'):
      return getattr(self,key)
    if key == 'width':
      try:
        return int(self.width)
      except:
        return 80
    if key == 'app_id':
      try:
        return int(self.app_id)
      except:
        return 3743872231
