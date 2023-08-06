import novotools.utils as tools
from functools import partial


# DocxApi
def docxapi_test():
    """
    test for DocxApi class
    """
    docxapi = tools.DocxApi()

    docxapi.set_font(en_style='Times New Roman',zh_style='微软雅黑')

    title_size = docxapi.get_pt_by_size("一号")
    title = docxapi.add_paras("Word操作测试")
    title = docxapi.align_center(title)

    docxapi.set_para_font_size(title,title_size)
    pic = docxapi.add_picture("./Python.png",2.5,2.5)
    pic = docxapi.align_center(pic)

    second_title_size = docxapi.get_pt_by_size("二号")
    second_title = docxapi.add_paras("段落示例")
    second_title = docxapi.set_para_font_size(second_title,second_title_size)
    docxapi.add_paras("在我所有的程序错误中，80%是语法错误，剩下20%里，80%是简单的逻辑错误，\
    在剩下4%里，80%是指针错误，只有余下的0.8%才是困难的问题。")

    table_list = [
        ["标题","内容"],
        ["DocxApi","使用python操作word文档"]
    ]
    second_title = docxapi.add_paras("表格示例")
    second_title = docxapi.set_para_font_size(second_title,second_title_size)

    docxapi.add_table(table_list)
    ofile = "docxapi_test.docx"
    docxapi.save(ofile = ofile)
    print(f"save docx to {ofile}")


def imap_test():
    """
    test for IMAPEMAIL class
    """
    imap = tools.IMAPEmail(
        user = "medical-sc-info@novogene.com",
        password = "HblM70kQjVb]tYL",
        receive_host = 'imap.exmail.qq.com',
        receive_port = 993,
    )
    
    imap.list_box()
    imap.search_email(
        search_key = "X101SC21072336-Z01-J004",
        box = "&UXZO1mWHTvZZOQ-/AutoPipeline",
        search_type="ALL",
        download_attach= False
    )

def send_email_test():
    """
    send email by send_email
    """
    send_email = partial(tools.send_email,
        **{
        "user" : "medical-sc-info@novogene.com",
        "password" : "HblM70kQjVb]tYL",
        "send_host" : 'smtp.exmail.qq.com',
        "send_port" : 465,
        }    
    )
    
    recipients = ["chenming@novogene.com"]
    subject = "send email test"
    text = "This is a test email for send_email function with attachment"
    files = ["docxapi_test.docx"]
    
    send_email(recipients=recipients,
               subject=subject,
               text=text,
               files=files)
    
def time_test():
    """
    TimeParser test
    """
    import datetime as dt
    
    print(tools.TimeParser.transfer_to("2021-10-22",to="string"))
    print(tools.TimeParser.transfer_to("2021-10-22 15:30:00",to="string"))
    print(tools.TimeParser.transfer_to("2021-10-22 15:30:00.01",to="string"))
    print(tools.TimeParser.transfer_to("2021-10-22 15:30:00.01",to="timestamp"))
    print(type(tools.TimeParser.transfer_to("2021-10-22 15:30:00.01")))
    print(str(dt.datetime.now()))
    print(type(tools.TimeParser.str_to_timedelta("17:55:18.806000")))
    print(type(tools.TimeParser.str_to_timedelta("1 day, 2:18:31.712400")))
    print(type(tools.TimeParser.str_to_timedelta("2 days, 2:18:31.712400")))
    

def title_parse_test():
    """
    test for TitleParser
    """
    title = "gene\tchromosome\tstart\tend\n"
    line = "Foo\t1\t100\t1000\n"
    tp = tools.TitleParser(title,split="\t")
    line_list = line.strip().split("\t")
    gene = tp.get_field(line_list,"gene")
    chr_idx = tp.get_idx("chromosome")
    have_start = tp.have_title("start")
    print(f"Gene name:{gene}; chromosome idx:{chr_idx}; have_start: {have_start}")

def run_cmd_test():
    cmd_normal = "ls ."
    stdout,stderr = tools.run_cmd(cmd_normal)
    print(f"{cmd_normal}标准输出为 {stdout}; 标准错误为 {stderr}")
    cmd_err = "cd not_exist_dir"
    stdout,stderr = tools.run_cmd(cmd_err)
    print(f"{cmd_err}标准输出为 {stdout}; 标准错误为 {stderr}")

def make_colors_test():
    colors = tools.make_colors()
    print(f"{colors['red']}[Warning] {colors['green']} [pass] {colors['cyan']} [info] {colors['back']} [normal]")

def datasize_convert_test():
    trans_size1 = tools.datasize_convert('1024G','T',return_type="float")
    trans_size2 = tools.datasize_convert('1024KB','B',return_type="int")
    trans_size3 = tools.datasize_convert('1024KB','GB',return_type="str")
    print(f"trans_size1 type :{type(trans_size1)}")
    print(f"trans_size2 type :{type(trans_size2)}")
    print(f"trans_size3 type :{type(trans_size3)}")

def basic_log_test():
    import logging
    logger = tools.basic_log("logger",level=logging.DEBUG)
    
    logger.debug("This message is for debug")
    logger.info("This is a information message")
    logger.warning("This is a warning")
    logger.error("This is a error")
    logger.critical("This is the badest conditon!")

def thread_enhance_test():
    
    from threading import current_thread
    
    @tools.thread_enhance()
    def func():
        print(f"Current threading:{current_thread().name}")
        print("start run ...")
        print(1/0)
        
    def func_test():
        th = func()
        th.start()
        th.join()
        
        if th.error != 0:
            print(th.msg)
        else:
            print("No error in thread")
            
        print("main thread end.")
    
    func_test()
    
if __name__ == "__main__":
    # imap_test()
    # send_email_test()
    # title_parse_test()
    # run_cmd_test()
    # make_colors_test()
    datasize_convert_test()
    basic_log_test()
    thread_enhance_test()