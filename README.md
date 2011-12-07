pybo
====
Play [weibo](http://weibo.com) just like Vi/Emacs.
Get & Run
---------
<pre><code>curl -0 https://raw.github.com/likang/pybo/master/pybo.py > pybo.py
python pybo.py
</code></pre>

Usage
-----
<pre>
| Key         | Action               |
|-------------|----------------------|
| Enter       | move down one line   |
| Space       | foreword one screen  |
| b or B      | back one screen      |
| q or Q      | quit                 |
| :command    | run command          |
</pre> 

Config File
-----------
Location: ~/.pybo  
Options :

* username  
* password  
* app\_id  
  The app id got from Sina, you can regist another app on [open.weibo.com](http://open.weibo.com), or just use mine.    
* width  
  Max width of the output
