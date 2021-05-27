#%%
import requests as req
import pandas as pd 
from datetime import datetime as dat
class notfication():
    params = dict(
            MainUri="https://api.telegram.org/bot1594781454:AAHjAonK53RbYW7Q7b538ilINhLeVaK9t64/",
            messageUri="https://api.telegram.org/bot1594781454:AAHjAonK53RbYW7Q7b538ilINhLeVaK9t64/sendMessage?chat_id=@WkingTech&text="
    )
    def __init__(self):
        a="hi"
    def sendMessage(self,id="@WkingTech",text="text not specify"):
        getreq=self.params['MainUri']+"sendMessage?chat_id="+id+"&text="+text
        res=req.get(getreq)
        return res
    
    def QuickSendMessage(self,text=' "text not specify" '):
        getreq=self.params['messageUri']+text
        res=req.get(getreq)
        return res

    # %%
bot=notfication()
bot.sendMessage(text="hi")
# %%

# %%
