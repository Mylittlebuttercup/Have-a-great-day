from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)


def getdatas(cur, result) : 
    result = result.fetchall()
    l = []
    for a in result :    
        d = {}
        fs = [c[0] for c  in cur.description ]
        for i in range(len(fs)) :
           d[fs[i]] = a[i]    
        l.append(d)
    return l
    
def getdatas1(cur, result) : 
    result = result.fetchall()
    
    a = result[0]
    
    d = {}
    fs = [c[0] for c  in cur.description ]
    
    for i in range(len(fs)) :
           d[fs[i]] = a[i]    
    return d



def runsql(sql) :
    conn =  sqlite3.connect("haveagreatday.db3")
    conn.set_trace_callback(print)
    cur =  conn.cursor()
    
    result = cur.execute(sql)
    return getdatas(cur, result)
    
def runsql1(sql) :
    conn =  sqlite3.connect("haveagreatday.db3")
    conn.set_trace_callback(print)
    cur =  conn.cursor()
    
    result = cur.execute(sql)
    return getdatas1(cur, result)
    

def executesql(sql) :
    conn =  sqlite3.connect("haveagreatday.db3")
    conn.set_trace_callback(print)
    cur =  conn.cursor()    
    cur.execute(sql)
    conn.commit()
    conn.close()


@app.route('/')
def index():

    db = runsql('SELECT * FROM product_tb')
    return render_template("main.html",   db = {'datas' : db})

@app.route('/todo')
def todo():

    db_t = {"datas" : runsql('SELECT * FROM todo_tb where do_ok = 1')}
    db_f = {"datas" : runsql('SELECT * FROM todo_tb where do_ok = 0')}    
    

    return render_template("todo.html",  db_t = db_t, db_f= db_f)

@app.route('/product')
def product():

    pid = int(request.args.get('pid'))    
    
    
    ret = runsql1(f'SELECT * FROM product_tb where pid={pid}')    
    print(ret)  
    return render_template("product.html",  db = ret)



@app.route('/product_buy')
def product_buy():

    pid = int(request.args.get("pid"))
    
    
    
    x = runsql1("SELECT * FROM user_tb where userid='minji'")    
    uid = x["uid"]
    


    x = runsql1(f'SELECT * FROM product_tb where pid={pid}')    
    pcoin = x["pcoin"]
    pname = x["pname"]
    
    
    
    executesql(f"update user_tb set lcoin=lcoin-{pcoin} where userid='minji'" )


    reg_date =  datetime.now().strftime("%m/%d/%Y, %H:%M:%S") 
    
    
    executesql(f"INSERT into buy_tb (uid, pid, pname, reg_date) values({uid}, {pid}, '{pname}', '{reg_date}')")
    
    
    

    

    html =   """
<script>  
     alert('buy ');
      window.location.href = '/product_list'
</script>
"""

    return html


@app.route('/product_list')
def product_list():


    db = runsql('SELECT * FROM buy_tb')
    print(db)

    ret = runsql1("SELECT * FROM user_tb where  userid='minji'")

    print(ret)


    return render_template("product_list.html",   
        db = {"datas" :db}, lcoin= ret["lcoin"] )
        
        
        



@app.route('/product_upload')
def product_upload():
    return render_template("product_upload.html")

@app.route('/product_upload_process', methods=["post"])
def product_upload_process():


    image = request.files['image']
    image_name = 'static/products/' + image.filename
    image.save(image_name)


    pname =  request.form.get('pname')    
    pcoin =  int(request.form.get('pcoin'))
    
    sql = f"INSERT into product_tb (pname, pcoin, image) values('{pname}', {pcoin}, '{image_name}')"
    executesql(sql)


    html = f"""

  제품 이미지 : {image.filename}  <br>
  <img  src={image_name}>
  제품 이름 : {pname}  <br>


  <a href=/> back  </a> 

"""

    return html


@app.route('/todo_upload')
def todo_upload():
    return render_template("todo_upload.html")


@app.route('/todo_complete')
def todo_complete():
   
    tid = int(request.args.get('tid'))
    tcoin = int(request.args.get('tcoin'))
    
    executesql(f"update todo_tb set do_ok = 1 where tid = {tid}")

    executesql(f"update user_tb set lcoin = lcoin + {tcoin} where userid='minji'")


    html =   """
 <script>  
     alert('complete');
      window.location.href = '/todo'
</script>
"""

    return html

@app.route('/todo_upload_process')
def todo_upload_process():
    
    title = request.args.get('title')
    tcoin = request.args.get('tcoin')


    sql =     f"INSERT into todo_tb (title, do_ok,  tcoin, uid) values('{title}', false, {tcoin}, 1)"
    print(sql)
    executesql(sql)
    

    return redirect('/todo')

if __name__ == '__main__':
    app.run(debug=True)


