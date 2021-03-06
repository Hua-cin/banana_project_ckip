from ckiptagger import WS, POS, NER
import os
import re
import jieba
import jieba.analyse
import datetime

t = []
t1 = """
余致榮不甘願辛苦種得香蕉任人喊價，也認為要做就做最好的，把香蕉產業從一把把進化到一根根。（圖由屏東縣政府提供）
〔記者陳彥廷／屏東報導〕傳統的水果行整把香蕉50元左右，但買回家易過熟，現在小家庭居多，也無法即時吃完，最後丟棄浪費，南州蕉農余致榮搭上輕食風，將香蕉切把分開賣，除了外銷日本，連便利商店也相中好攜帶食用的切把香蕉，市場通路大開。
40歲出頭的余致榮，祖父輩就已開始種香蕉，從小看著香蕉長大，卻曾「討厭」香蕉，後來也當到紡織廠經理，但10年前母親生病，他回家接手，沒想到從此成為興趣，2年前他與通路商合作，將外銷日本的香蕉切把，約5條1小包，到日本就能直接上架，而多的1、2根香蕉則看準小家庭，直送國內的便利超商。
余致榮表示，從2月到6月生產的冬蕉品質最好，也是外銷黃金期，現在一星期外銷一貨櫃，還供量販超市、批發市場等，不但賣綠香蕉也幫客戶摧熟。
余致榮現在有近10公頃蕉田，他說，原本討厭香蕉，現在卻變成他的專業，向香蕉研究所請益後，運用施肥克服連做問題，更解決黃葉病，同一塊地竟能連種4年香蕉，也讓他獲得「施肥達人」頭銜。
余致榮不甘願辛苦種得香蕉任人喊價，也認為要做就做最好的，把香蕉產業從一把把進化到一根根，他認為香蕉市場還有空間，現在他的洗選場成立，一年四季都能供應國內香蕉。
余致榮不甘願辛苦種得香蕉任人喊價，也認為要做就做最好的，把香蕉產業從一把把進化到一根根。（圖由屏東縣政府提供）
"""

t2 ="""

屏東農業再升級，與日本合作研發出香蕉抗性澱粉，讓香蕉又多了一個銷售管道（記者葉永騫攝）
〔記者葉永騫／麟洛報導〕屏東永信合作社與日本Vantek社長林原克明博士合作，從香蕉研製出香蕉抗性澱粉，有助消化系統功能，該商品已取得專利在日本上市，台灣也將跟進上市，今天舉行發表會，縣長潘孟安特別到場祝賀。
縣長潘孟安表示，屏東種植香蕉面積約3000公頃，佔全國第一，像夏蕉如果遇到外銷不順就會出現過剩問題，如果能夠加工來增加價值，對農民是一大喜訊，屏東縣正努力將農作物升級、加工、強化行銷，將屏東農產品外銷到國外，相當樂見農產品加工研發升級。
屏東永信合作社主席邱永豐說，這次與日本Vantek社長林原克明博士合作，將青香蕉連皮製成香蕉抗性澱粉，加入牛奶等飲料能夠增加飽足感，尤其是香蕉抗性澱粉能夠通過小腸和胃，對於腸胃消化系統特別有助益，為了確保品質，也和屏東農民契作，有效穩定國內香蕉市場調節。
林原克明則指出，香蕉抗性澱粉是目前各國研發的重點，對於這項產品問世相當有興趣，在日本食品展時各國都爭相詢問了解，未來的發展性相當大。
香蕉抗性澱粉有助於消化系統，能增加飽足感。（記者葉永騫攝）
屏東的香蕉研製成香蕉抗性澱粉，將成為新商品。（記者葉永騫攝）
"""

t3 = """
余致榮不甘願辛苦種得香蕉任人喊價，也認為要做就做最好的，把香蕉產業從一把把進化到一根根。（屏東縣政府提供）
〔記者陳彥廷／屏東報導〕傳統的水果行整把香蕉五十元到百元不等，但買回家易放到過熟，現在小家庭也無法即時吃完，南州蕉農余致榮搭上輕食風，將香蕉切把分開賣，除了外銷日本，連便利商店也相中好攜帶食用的切把香蕉。
余致榮從祖父輩就已開始種香蕉，從小看香蕉長大，卻曾經「討厭」香蕉，十年前母親生病，他回家接手從此成興趣，兩年前他與通路商合作，將外銷日本的香蕉切把，約五條一小把包好，到日本就能直接上架，而多的一、兩根香蕉則看準小家庭，直送國內的便利超商。
余致榮現在有近十公頃蕉田，他說，原本討厭香蕉，現在卻變成他的專業，向香蕉研究所請益後，解決黃葉病，讓他獲得「施肥達人」頭銜。
余致榮不甘願辛苦種的香蕉任人喊價，堅持要做就做最好的，把香蕉產業從一把把進化到一根根，他認為香蕉市場還有空間，現在他的洗選場成立，一年四季都能供應香蕉。
"""

t4 = """
屏東農業再升級，與日本合作研發出香蕉抗性澱粉，讓香蕉又多了一個銷售管道。（記者葉永騫攝）
取得專利 已在日本上市
〔記者葉永騫／麟洛報導〕屏東永信蔬果運銷合作社與日本Vantek社長林原克明博士合作，從香蕉研製出香蕉抗性澱粉，該商品已取得專利在日本上市，台灣也將販售，昨天舉行發表會，縣長潘孟安特別前往祝賀。
潘孟安表示，屏東種植香蕉面積約三千公頃，佔全國第一，但夏蕉如果遇到外銷不順時常出現過剩問題，如果能加工提高價值，對農民是一大喜訊，屏東縣正努力將農作物升級、加工、強化行銷，將農產品外銷到國外，樂見香蕉產業升級。
屏東永信合作社主席邱永豐說，該合作社的會員約一百人多數為農民，以運輸香蕉、檸檬、金桔等作物為主，這次與日本Vantek社長林原克明博士合作，將青香蕉連皮製成香蕉抗性澱粉，加入牛奶等飲料就能夠增加飽足感，尤其是香蕉抗性澱粉能夠通過小腸和胃，到大腸後協助排便，為了確保品質和供貨的穩定，也和合作社內農民契作了五百公頃，有效穩定國內香蕉市場調節。
林原克明指出，香蕉抗性澱粉是目前各國研發重點，該產品在日本食品展發表時，各國業者都爭相詢問，未來發展性相當大。
"""

t5 ="""
香蕉價格下跌，莿桐鄉公所週六上午將舉辦促銷活動。（記者詹士弘攝）
〔記者詹士弘／莿桐報導〕風調雨順也會傷農！莿桐香蕉豐收，種植面積從兩年前的四十公頃成長至一百公頃，導致價格疲弱，批發價從今年初每公斤四十元跌到目前十八元，公所將辦農特產品展售促銷。
莿桐果菜合作社理事長蘇明利表示，莿桐土壤肥沃，又有濁水溪水灌溉，非常適合種植香蕉，經他十年推廣，加上近年香蕉價格看悄，莿桐香蕉種植面積，也從四十公頃成長到現在的一百公頃，香蕉品質極佳，在台北批發市場都能賣出好價錢。
今年台灣遭逢罕見大旱，開春至今降雨量少，香焦每棵產量由二十公斤成長至三十公斤，但也因此供需失調，價格已從春節前每公斤四十元，跌到目前的十八元，價格是近年最差的一次。
莿桐鄉公所將於二十三日早上在莿桐公園舉辦「愛母親，護母河」珍貴水資源暨農特產品系列活動，鄉長廖秋蓉呼籲民眾踴躍參加。
"""

t6 ="""
原本每公斤近30元的香蕉，經颱風「歪腰」肆虐，價格恐再飆漲。（記者邱芷柔攝）
〔記者邱芷柔／屏東報導〕颱風蘇迪勒在全台刮起強陣風，台北市郵筒被招牌砸中後的「歪腰」模樣，讓民眾直呼好可愛，意外引起排隊KUSO搶拍，而以農立縣的屏東，香蕉、木瓜下個月就能採收，沒想到強風攪局，讓農民直呼，「同樣都是歪腰，但我們真的笑不出來！」
內埔鄉果農沈文彬說，強陣風從8日清晨開始連刮十幾個小時，木瓜、香蕉約再1個月就能採收，現在幾乎全軍覆沒，而且沒有一個農民的農地倖免，即使存活下來的果樹，也因為枝葉受損無法再輸送養份，無論國內市場或外銷市場都受到影響。
農民指出，1公頃的木瓜園約需投注70至80萬的成本，雖然農糧署補助不無小補，但依據過去經驗，每公頃補助僅6、7萬，且申請補助手續繁雜、核定速度又慢，農民多只能自行吸收，捲起袖子從頭再來。
屏東縣政府農業處處長姚志旺指出，今早已派員下鄉持續統計縣內農損情形，目前得知受損最嚴重的是香蕉與木瓜，受害面積已逾1百公頃且統計數量持續攀升中，颱風前香蕉每公斤近30元，木瓜每公斤約20元，價格平穩，颱風過後因供需失衡，價格勢必看漲。
姚志旺也表示，農糧署與縣府人員會在最短時間內協助農損核定，也呼籲農民儘速回報農損情形，保障自己的權益。
農民直呼「同樣都是歪腰，但我們真的笑不出來！」（記者邱芷柔攝）
"""

t7 ="""
梅姬颱風重創國姓鄉香蕉產業，長流村受風面的香蕉園幾乎全部攔腰折斷。（記者佟振國攝）
〔記者佟振國／南投報導〕全倒了！梅姬颱風狂掃，南投縣國姓鄉香蕉受災嚴重，公所估計全鄉311公頃受災面積即逾100公頃，主要是倒伏與葉片受損，平均受損程度近3成，且災情陸續傳回，嚴重程度可能再攀升，長流村位處受風面的香蕉園幾乎全倒，農民忙了大半年，再過1個月就能收成的心血全泡湯，只能苦笑「梅姬颱風真的讓農民沒錢（台語）了。」
國姓鄉香蕉栽種面積達311公頃，是鄉內單一果樹面積最大的，主要集中於長流、北港、大石等村，長流村長羅廣霖表示，這次梅姬颱風帶來強勁北風，27日一整天不時颳起強陣風，位於北側的長流村首當其衝，高莖作物香蕉、玉米受損嚴重。
農民邱金田栽種5、6分地的香蕉園約有500株，僅10株尚未長大的香蕉樹倖存，其餘全部攔腰折斷，受損程度達98％；農民邱見明栽種400株，許多都已經結芎包袋，預計再過1個月就能收成，大部分都被颱風吹倒，有些未倒的也因為葉片受損無法行光合作物，果實不會再成長，形同廢果，受損程度也超過8成。
農民無奈表示，冬季香蕉的價格一向看俏，前一陣子每百公斤批發價平均有4500元至5000元左右，有些甚至來到6500元，現在全被梅姬颱風收走了，砍除重新發芽生長，最快也要到明年4、5月才有收成。
公所指出，初估全鄉香蕉311公頃受災面積達100公頃，平均受損程度在25％至30％，已達現金救助標準，災情陸續回報可能還會向上攀升，從今天起至10月11日受理農民申報。
相關影音

面對心血全部泡湯，農民心在淌血，也只能砍掉重練。（記者佟振國攝）
再過1個月就能收成的香蕉，因為植株倒伏及葉片受損，無法再長大，形成廢果。（記者佟振國攝）
"""

t8 ="""
今年元旦香蕉價格飆到每公斤86元，創下20年新高，昨天又漲到100.9元，創下史上最高價。
（資料照，記者陳鳳麗攝）
〔記者林彥彤／台北報導〕今年元旦香蕉批發價格才飆到每公斤八十六元，半個月後，昨天飆破一百元，創下史上最高價。農糧署表示，漲價除了與颱風有關外，這次又碰到氣溫驟降，生產量降低影響到貨量，造成價格短期內大漲，呼籲民眾改買其他類水果。
根據農產品批發市場交易網站顯示，昨天水果平均每公斤七十六元，其中香蕉每公斤貴到一○○．九元（去年同期五十四．九元），其他水果也現漲勢。同樣遭受颱風重創而持續漲價的棗子，每公斤七十八元（去年同期四十．四元），釋迦更漲到一○一元（去年六十五．二元），民眾春節前採買水果，要有心理準備。
價格回穩要等到三、四月產季
農糧署副署長蘇茂祥說明，受颱風影響，水果受損嚴重，加上最近氣溫驟降，香蕉生產速度更慢，導致昨天交易量僅一萬五千五百五十一公斤，較去年同期二萬六千四百四十八公斤減少很多，因此價格大漲，預計要等到三、四月產季，民眾才吃得到平價香蕉。
消費者楊先生表示，市場買五根香蕉就要一○八元，很嚇人；也了解冬天的香蕉價格多少會受夏天風災影響。但不能理解的是，明明政府預期會發生，卻年年無對策？蘇茂祥無奈指出，政府並非沒有對策，而是受限於「檢疫」問題，無法以進口平衡供需，加上水果替代性高，僅能呼籲民眾改買當季水果。
另外，蔬菜昨天每公斤平均十八．七元（去年同期卅三．九元），高麗菜每公斤六．八元，也較去年同期十四．六元便宜。
蘇茂祥說，蔬菜去年受霸王級寒流影響，罕見地高漲，今年的價格回到正常。為避免過剩，政府鎖定日本、新加坡與香港等國外銷高麗菜，希望能幫助農民提高收益。
"""

t9 = """
台農發公司董事長陳郁然今天表示，要有質量穩定的規模經濟，才能做好外銷。未來荔枝、香蕉、印度棗、鳳梨、鳳梨釋迦及芭樂等水果都在評選範圍內；但香蕉是最重要的選項。
台灣肥料股份有限公司子公司重組清算，農業委員會在今年8月18日完成公司更名登記，輔導成立「台灣國際農業開發股份有限公司」，額定資本額為新台幣10億元，今天舉辦成立記者會。
第一階段邀集與農產外銷相關企業及單位擔任策略股東，已募集1億5200萬元，公司董、監事席次為董事7人及監察人2人，聘請具外銷實務經驗的紐西蘭奇異果公司前總裁陳郁然擔任董事長。
農委會主委曹啟鴻表示，台灣農業有得天獨厚的基礎，從日據時代打下基礎、農復會時代美方給予協助，盼整合台灣的生產、集貨到行銷，讓農業再精進發展。
陳郁然表示，產官學媒談台灣農業發展很多年了，但沒有既定的方向，農民間又互相競爭外銷價格，不能整合下也難保合理利潤，且過去台灣農產銷售只管內銷，投資機會偏向同樣說中文的中國大陸，政治操作好的時候，市場呈現一片榮景，不好的時候抱怨政府。
他以服務過的紐西蘭奇異果的金果為例，生產成本比綠果低，但價值多50%，收成利潤比綠果多4倍，就因為它有競爭優勢。
他並說，台灣過去有過香蕉外銷榮景，卻因台灣一直有香蕉，所以台灣人不知道香蕉在美、歐等各國市場都很重要，它是最重要的作物；但台灣要有質量穩定的規模經濟，才能做好外銷。
林全致詞時表示，台灣農業成就工業發展，也在外交上扮演重要角色，但地小、生產力不足，大部份農民所得偏低，變成「兼業農」；農業需要根本改變，把農業資源做整合；而台農發公司最重要的使命，就是要把農業往現代化推進。
他強調，成立公司之初，他讀了一些文件，發現農業最大的榮景仍是過去的香蕉外銷年代，而陳郁然告訴他，「我們只看到市場，沒有看到背後生產的農民、生產面問題，要外銷產品，要先跟農民、生產面變成一個團隊，品質跟數量一定要穩定，不然產品會變成今年有、明年沒有，要做好這些，農產才能推廣到海外。」
林全期許，台農發公司要進一步發展要把新的經營手法引入台灣，包含智慧科技，而台灣農業要走出國外、不只自我保護，要將產銷供應體系整合起來，以國家品牌外銷，並讓更多年輕人進入農業，打造新農業。
陳郁然會後受訪指出，台灣合作農業生產與銷售的國家，從東南亞到南半球都有，作物從荔枝、香蕉、印度棗、鳳梨、鳳梨釋迦及芭樂都在評選範圍內，連農業資材與技術都是外銷產品；但是香蕉是最重要的選項。
台農發公司任務計3大項，包含「農產品進出口」、「技術輸出」及「海外投資與資材外銷」。農委會副主委陳吉仲說，未來也會協助農委會於風災前後專案進口大宗與根莖類蔬菜，穩定市場需求與價格。1051205
(中央社)
"""

t10 = """
財團法人21世紀基金會今召開記者會表示，將針對民進黨立委段宜康的諸多不實指控提出告訴。（資料照，記者羅沛德攝）
〔即時新聞／綜合報導〕財團法人21世紀基金會今召開記者會表示，將針對民進黨立委段宜康的諸多不實指控提出告訴，該基金會執行長孫明賢除出席記者會，也在23日晚間播出的政論節目中提到，台灣的農業早在10年前就被中國超越了，且基金會是公益性團體，不可能去投資或認股，而農業技術及農業科技都是要拿來賺錢的。
立委段宜康近日在臉書指出，國民黨總統候選人朱立倫的岳父高育仁擔任「二十一世紀基金會」董事長時，從事兩岸農業生意將台灣農業技術交給中國，甚至提出相關問題質疑，21世紀基金會是否與中國農業科學院、福建農業科學院，一起出資15億人民幣（76億2100萬台幣）打造兩岸農產品交易和農業技術交流平台，但對於這些指控孫明賢今除召開記者會揚言提告段宜康，也在壹電視23日晚間播出的《正晶限時批》中回應外界質疑。
據了解，孫明賢在節目中不斷強調，該基金會是公益性團體，不可能去投資或認股，更不會有段宜康所言的技術股存在，針對基金會是否與中方的農科院出資打造兩岸農業交流平台，他也表示一毛錢都沒出，只是搭建可供技術交流的平台。
針對現場來賓質疑，台灣農業的品種、技術在身兼21世紀基金會執行長、亞蔬中心的理事長及海峽兩岸農業交流協會顧問的孫明賢手中外流給中國，孫則一概否認，並指品種、技術不在他手上，強調基金會只是提供技術服務，外流的責任不在他。
雖然現場來賓質疑，若台灣的技術、品種沒有中國好，中國為何還要找台灣合作，但孫明賢表示，其實中國的農科發展早在10年就已超越台灣，所謂全世界最好吃的水果，只有不到10個熱帶水果，其他的品種台灣沒有一樣比中國好。孫甚至說，中國跟其他國家都有合作，其實不必靠台灣的品種、技術，且許多水果都是南部綠營執政的縣市長賣到中國去的，而最好的水果就是最好的品種，但像全世界都在種的富士蘋果，日本也沒說品種被偷走了。
孫明賢也針對立委葉宜津近日的發言指出，她所談的香蕉問題完全是錯誤的，因為中國沒有香蕉銷往日本，替代台灣銷到日本的香蕉是出自菲律賓，且台灣的香蕉也不是被菲律賓打垮的，而是自己打垮了，因為民進黨執政時開放了貿易公司出口香蕉，才會自己打垮自己。孫明賢還說，香蕉、茶葉的品種其實全部都是19世紀從中國來的。
孫明賢也說，兩岸農業合作啟動是1990年開始，但中間歷經政黨輪替，至今仍無哪一個政府明定有什麼品種、技術不可以過去。孫明賢說，品種、技術都在農民手上，農民要拿去哪裡種也不能怎麼樣，且他認為品種研發唯一的目的就是賺錢，沒有專利權的東西誰都可以拿得到。針對現場來賓王瑞德詢問「所以是台灣的農民賺錢還是中國的農民賺錢」？孫明賢則回應，「不管，誰拿去就誰賺錢」。
孫明賢表示，其實中國的農科發展早在10年前就已超越台灣，所謂全世界最好吃的水果，只有不到10個熱帶水果，其他的品種台灣沒有一樣比中國好。（圖擷自壹電視）
"""

t.append(t1)
t.append(t2)
t.append(t3)
t.append(t4)
t.append(t5)
t.append(t6)
t.append(t7)
t.append(t8)
t.append(t9)
t.append(t10)

counter = 0

def func_jieba(text):
    '''
    :param text:
    :return: word count dict
    '''

    # fetch stop word list
    stopword_path = r'./01_ref_data/stopword.txt'
    stopword_list = []
    with open(stopword_path, 'r', encoding='utf-8') as f_stop:
        for temp in f_stop.readlines():
            stopword_list.append(temp.replace('\n', ''))

    # fetch mydict list
    jieba.load_userdict(r'./01_ref_data/mydict.txt')
    s = jieba.cut(text)
    jieba_word_count = {}

    for i in s:
        if i in jieba_word_count:
            jieba_word_count[i] += 1
        else:
            jieba_word_count[i] = 1
    # filter jieba wordcut list by user define
    jieba_word = [(k, jieba_word_count[k]) for k in jieba_word_count if (len(k) > 1) and (k not in stopword_list) and not re.match(r'[0-9a-zA-Z]+',k)]

    # sort jieba wordcut list
    jieba_word.sort(key=lambda item: item[1], reverse=True)

    # init jieba wordcut dict
    jieba_dict = {}

    # insert data to jieba wordcut dict
    for i in jieba_word:
        jieba_dict[i[0]] =i [1]

    print(jieba_dict)

    # return word cut result by dict
    # return jieba_dict


def func_ckip_muti(user, task_queue):
    '''
    text to sorted list
    '''

    while True:

        text = task_queue.get().replace('\n', ' ')

        # insert stopword list
        stopword_path = r'./01_ref_data/stopword.txt'
        stopword_list = []
        with open(stopword_path, 'r', encoding = 'utf-8') as f_stop:
            for temp in f_stop.readlines():
                stopword_list.append(temp.replace('\n', ''))

        ws = WS("../data")
        ws_results = ws([text])

        ckip_word_count = {}
        for i in ws_results[0]:
            if i in ckip_word_count:
                ckip_word_count[i] += 1
            else:
                ckip_word_count[i] = 1

        ckip_word_list = [(k, ckip_word_count[k]) for k in ckip_word_count if
                          (len(k) > 1) and (k not in stopword_list) and not re.match(r'[0-9a-zA-Z]+', k)]
        ckip_word_list.sort(key=lambda item: item[1], reverse=True)

        ckip_dict = {}
        for i in ckip_word_list:
            ckip_dict[i[0]] =i[1]

        print("{}:{}".format(user, ckip_dict))
        task_queue.task_done()

    # return ckip_dict


# ckip_start = datetime.datetime.now()
# for i in t:
#     print("{}".format(func_ckip(i)))
# ckip_end = datetime.datetime.now()
# ckip_spend = ckip_end-ckip_start
# print("ckip spend : {} ".format(ckip_spend))
#
#
# jieba_start = datetime.datetime.now()
# for i in t:
#     print("{}".format(func_jieba(i)))
# jieba_end = datetime.datetime.now()
# jieba_spend = jieba_end-jieba_start
# print("jieba spend : {} ".format(jieba_spend))
#
# print("****************************")
# print("ckip spend : {} ".format(ckip_spend))
# print("jieba spend : {} ".format(jieba_spend))
#
# print("ckip slow jieba :{}".format(ckip_spend-jieba_spend))
# print("{}".format(ckip_spend/jieba_spend))




import multiprocessing as mp
import os, random, time

counter = 0



def main():
    # 任務佇列
    task_queue = mp.JoinableQueue()

    worker1 = mp.Process(target=func_ckip_muti,args=(1, task_queue))
    worker1.daemon = True
    worker1.start()

    worker2 = mp.Process(target=func_ckip_muti,args=(2, task_queue))
    worker2.daemon = True
    worker2.start()

    worker3 = mp.Process(target=func_ckip_muti,args=(3, task_queue))
    worker3.daemon = True
    worker3.start()

    worker4 = mp.Process(target=func_ckip_muti,args=(4, task_queue))
    worker4.daemon = True
    worker4.start()

    for i in range(10):
        task_queue.put(t[i])
        print(t[i])
    print("----")
    print(task_queue)
    print("----")

    task_queue.join() # 確定 PM 已經交付任務完畢

    print("----")
if __name__=="__main__":
    ckip_start = datetime.datetime.now()

    main()
    ckip_end = datetime.datetime.now()
    ckip_spend = ckip_end-ckip_start
    print("ckip spend : {} ".format(ckip_spend))


# ckip_start = datetime.datetime.now()
# for i in t:
#     print("{}".format(func_ckip(i)))
# ckip_end = datetime.datetime.now()
# ckip_spend = ckip_end-ckip_start
# print("ckip spend : {} ".format(ckip_spend))
