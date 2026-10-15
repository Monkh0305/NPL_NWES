"""Sports project deck using the supplied PriceHunter PDF as a visual reference."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
exec((ROOT/'build_slides.py').read_text(encoding='utf-8').split('# 01 — cover')[0])
ORANGE='F07818'; MINT='EAF8F2'; CREAM='FFF4E9'; GRAY='F5F6F9'
INK='19253D'; MUTED='697180'; TEAL='299C7D'; WHITE='FFFFFF'
prs.core_properties.title='SPORTS INSIGHT | วิเคราะห์เสียงแฟนกีฬาด้วย AI'
prs.core_properties.subject='การนำเสนอโครงงาน — รูปแบบอ้างอิง PriceHunter'
original_text=text
def text(s,txt,x,y,w,h,size=22,bold=False,c=INK,align=None):
    shape=original_text(s,txt,x,y,w,h,size,bold,c,align)
    for p in shape.text_frame.paragraphs:
        for r in p.runs:
            props=r._r.get_or_add_rPr()
            for tag in ['a:ea','a:cs']:
                element=OxmlElement(tag); element.set('typeface',FONT); props.append(element)
    return shape

def bg(s,x,y,w,h,fill=GRAY):
    shape=box(s,x,y,w,h,fill,radius=True)
    sp=shape._element.spPr
    sp.append(OxmlElement('a:effectLst'))
    return shape

def page(title,section,dark=False):
    s=prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid(); s.background.fill.fore_color.rgb=color(INK if dark else WHITE)
    text(s,section,.65,.42,11,.3,11,True,TEAL if dark else ORANGE)
    if title:
        text(s,title,.65,.93,12,1.0,29,True,WHITE if dark else INK)
        box(s,.67,1.87,.78,.045,ORANGE)
    text(s,'SPORTS INSIGHT  /  NLP PROJECT',.67,7.12,10,.2,8,False,'A6AEBB' if dark else MUTED)
    text(s,f'{len(prs.slides):02}',12,7.08,.6,.28,10,False,MUTED,PP_ALIGN.RIGHT)
    return s

def card(s,x,y,w,h,title,body='',fill=GRAY,index=None):
    bg(s,x,y,w,h,fill)
    top=y+.25
    if index:
        bg(s,x+.22,top,.48,.43,MINT if fill==WHITE else WHITE)
        text(s,index,x+.22,top,.48,.42,15,True,TEAL,PP_ALIGN.CENTER)
        top+=.64
    text(s,title,x+.25,top,w-.5,.78,21,True)
    if body: text(s,body,x+.25,top+.91,w-.5,h-(top-y)-1.02,16,False,MUTED)

def ribbon(s,txt,fill=GRAY):
    bg(s,.7,6.27,11.94,.53,fill)
    text(s,txt,.93,6.34,11.5,.37,14,False,MUTED)

def circles(s):
    for x,y,d,c in [(9.7,-.1,3.6,CREAM),(9.1,4.8,2.25,MINT)]:
        # Keep decorative circles within the canvas.
        y=max(0,y)
        sh=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x),Inches(y),Inches(d),Inches(d))
        sh.fill.solid(); sh.fill.fore_color.rgb=color(c); sh.line.fill.background()

s=page('','SPORTS PROJECT / NATURAL LANGUAGE PROCESSING')
circles(s); box(s,0,0,.13,7.5,ORANGE)
text(s,'SPORTS INSIGHT',.8,1.45,9.2,.9,44,True)
box(s,.82,2.62,.045,.55,ORANGE)
text(s,'อ่านเสียงแฟนกีฬา ด้วย AI',1.05,2.59,9,.7,29,True)
text(s,'จากความคิดเห็นบน YouTube\nสู่ภาพรวมที่เข้าใจง่าย',.85,3.7,7.9,1.35,26,False,MUTED)
for i,(t,c) in enumerate([('YouTube',CREAM),('Gemini API',MINT),('React + FastAPI',GRAY)]):
    bg(s,.85+i*2.45,5.52,2.2,.47,c); text(s,t,.95+i*2.45,5.57,2,.3,12,True)
note(s,'แนะนำโครงงานเว็บวิเคราะห์ความคิดเห็นต่อวิดีโอกีฬาบน YouTube ชื่อ SPORTS INSIGHT ใช้เป็นชื่อในการนำเสนอ ระบบเดิมใช้ Gemini API วิเคราะห์ภาษา รูปแบบภาพอ้างอิงจากไฟล์ PriceHunter ของผู้ใช้ แต่เนื้อหาเป็นของโครงงานกีฬา')

s=page('คอมเมนต์มากมาย แต่ภาพรวมยังอ่านยาก','01 / ปัญหา')
for i,t in enumerate(['ความคิดเห็นกระจัดกระจาย','มีทั้งคำชม คำถาม และคำวิจารณ์','บริบทกีฬาเปลี่ยนความหมายของคำ']):
    box(s,.8,2.56+i*.9,.09,.09,ORANGE); text(s,t,1.1,2.4+i*.9,6.4,.65,23,True)
card(s,8,2.35,4.6,2.6,'“แฟน ๆ รู้สึกอย่างไร?”','อ่านทีละข้อความ\nยังตอบภาพรวมได้ยาก',CREAM)
ribbon(s,'เป้าหมาย: เปลี่ยนข้อความจำนวนมากให้เป็นภาพรวมที่สำรวจต่อได้')
note(s,'ปัญหาที่โครงงานต้องการแก้คือการอ่านความคิดเห็นทีละข้อความทำให้เห็นภาพรวมได้ยาก บริบทเกี่ยวกับนักกีฬา ทีม หรือกรรมการอาจเปลี่ยนความหมายของข้อความ คำถามด้านขวาเป็นคำถามตั้งต้น ไม่ใช่คำพูดจากผู้ใช้ที่สัมภาษณ์')

s=page('ออกแบบเพื่อคนที่อยากเข้าใจเสียงผู้ชม','02 / ผู้ใช้และคุณค่า')
for i,(a,b) in enumerate([('ผู้สร้างคอนเทนต์','สำรวจเสียงตอบรับ\nต่อวิดีโอกีฬา'),('ผู้สนใจกีฬา','ดูความรู้สึกและ\nประเด็นที่คนพูดถึง'),('ผู้ศึกษา NLP','สำรวจผลวิเคราะห์\nและข้อจำกัดของภาษา')]):
    card(s,.7+i*4.1,2.4,3.75,3.05,a,b,[CREAM,MINT,GRAY][i],str(i+1))
ribbon(s,'กลุ่มผู้ใช้ที่ออกแบบไว้ • ยังไม่ได้สรุปจากการทดสอบผู้ใช้จริง')
note(s,'กลุ่มนี้เป็นผู้ใช้เป้าหมายตามลักษณะงาน ไม่ใช่ผลวิจัยความต้องการหรือหลักฐานการยอมรับจากผู้ใช้ ระบบช่วยสำรวจข้อมูล ไม่ตัดสินแทนคนทั้งหมด')

s=page('เลือกวิดีโอ แล้วให้ AI ช่วยอ่านความคิดเห็น','03 / แนวคิดของระบบ')
bg(s,.7,2.3,11.9,1.05,CREAM)
text(s,'YouTube  →  ความคิดเห็น  →  Gemini  →  ภาพรวม',1,2.55,11.3,.6,27,True)
for i,(a,b) in enumerate([('ความรู้สึก','บวก / กลาง / ลบ'),('อารมณ์','เช่น ยินดี โกรธ เศร้า'),('ประเด็นสำคัญ','หัวข้อ คำสำคัญ สรุปไทย')]):
    card(s,.7+i*4.1,3.8,3.75,2.05,a,b,WHITE)
note(s,'ระบบส่งข้อความให้ Gemini จำแนก sentiment และ emotion รวมทั้งประเด็นและคำสำคัญ จากนั้นแสดงกราฟและสรุปภาษาไทย ไม่ได้โหลดหรือฝึกโมเดลภายในเครื่อง')

s=page('ผู้ใช้ทำเพียง 3 ขั้นตอน','04 / USER FLOW')
for i,(a,b) in enumerate([('ค้นหาคลิปกีฬา','ค้นหา / เลือกหมวด'),('เลือกวิดีโอ','เปิดคลิปที่สนใจ'),('กดวิเคราะห์','อ่านกราฟและสรุป')]):
    card(s,.75+i*4.12,2.6,3.55,2.8,a,b,MINT if i==2 else CREAM,str(i+1))
    if i<2: arrow(s,4.48+i*4.12,3.65,.3,.3,ORANGE)
ribbon(s,'ผลลัพธ์รวมอยู่ในหน้าแดชบอร์ดเดียว')
note(s,'นำผู้ฟังตามขั้นตอนการใช้งานจริง เริ่มค้นหาวิดีโอกีฬา เลือกคลิป แล้วกดวิเคราะห์ การเรียกวิเคราะห์ต้องมีคีย์ Gemini และต้องรอการตอบกลับจากบริการภายนอก')

s=page('ดึงข้อความ → วิเคราะห์ → ตรวจสอบ → แสดงผล','05 / AI PIPELINE')
for i,(a,b) in enumerate([('YouTube API','ความคิดเห็นหลัก'),('Gemini API','Structured JSON'),('ตรวจสอบ','Schema + ID'),('Dashboard','กราฟ + สรุปไทย')]):
    card(s,.7+i*3.08,2.6,2.7,2.7,a,b,MINT if i==3 else GRAY,f'0{i+1}')
    if i<3: arrow(s,3.46+i*3.08,3.7,.23,.25,ORANGE)
ribbon(s,'ค่าเริ่มต้น: สูงสุด 100 ความคิดเห็น / รอบ • สูงสุด 2,000 ตัวอักษร / ความคิดเห็น',CREAM)
note(s,'อ้างอิง README.md ระบบใช้วิดีโอหมวด Sports ส่งตัวอย่างความคิดเห็นหลักสูงสุดตามค่าตั้งต้น 100 รายการ จำกัด 2000 ตัวอักษรต่อรายการ Backend ตรวจรูปแบบ JSON และความครบถ้วนของผลสำหรับทุกความคิดเห็นก่อนคำนวณสัดส่วนและบันทึก')

s=page('ตรวจข้อมูลก่อนเปลี่ยนเป็นกราฟ','06 / ความน่าเชื่อถือของผล')
for i,(a,b) in enumerate([('รูปแบบถูกต้อง','JSON Schema + Pydantic'),('ผลครบทุกข้อความ','ตรวจ ID และป้ายกำกับ'),('คำนวณจากตัวอย่าง','จำนวนในกลุ่ม ÷ n × 100')]):
    card(s,.7+i*4.1,2.5,3.75,2.7,a,b,[MINT,CREAM,GRAY][i],str(i+1))
ribbon(s,'หาก API ล้มเหลวหรือผลไม่ครบ ระบบแจ้งข้อผิดพลาด',MINT)
note(s,'การตรวจสอบรูปแบบไม่ใช่การรับรองความแม่นยำด้านภาษา Backend ตรวจ ID ให้ครอบคลุมข้อมูล ตรวจ label ตามชุดที่อนุญาต คำนวณเปอร์เซ็นต์จากผลจริง และไม่บันทึกผลปลอมเมื่อบริการขัดข้อง หนึ่งความคิดเห็นมีได้หลายหัวข้อ สัดส่วนหัวข้อจึงอาจรวมเกิน 100 เปอร์เซ็นต์')

s=page('เทคโนโลยีที่ทำงานร่วมกัน','07 / TECH STACK')
for i,(a,b) in enumerate([('หน้าเว็บ','React\nVite'),('Backend','FastAPI\nPydantic'),('AI / ข้อมูล','Gemini API\nYouTube Data API'),('จัดเก็บผล','SQLite\nผลวิเคราะห์')]):
    card(s,.7+i*3.08,2.45,2.72,3.25,a,b,MINT if i==2 else GRAY,f'0{i+1}')
ribbon(s,'คีย์ API อยู่ฝั่ง Backend • ไม่ต้องรันโมเดลในเครื่อง')
note(s,'สถาปัตยกรรมอ้างอิง README ของโปรเจกต์ Frontend ติดต่อ FastAPI ซึ่งประสานงาน YouTube และ Gemini ก่อนจัดเก็บผลใน SQLite API keys ไม่ถูกส่งให้ frontend')

s=page('หน้าจอจริง: ค้นหาและเลือกวิดีโอ','08 / DEMO · ค้นหา')
photo(s,'dashboard.png',.8,2.1,9.45,4.78)
text(s,'01  ค้นหา\n\n02  เลือกคลิป\n\n03  วิเคราะห์',10.25,2.9,2.7,2.9,19,True)
note(s,'ภาพจาก presentation/assets/dashboard.png เป็นภาพที่บันทึกไว้ในโปรเจกต์ ไม่ใช่ระบบสดขณะนำเสนอ อธิบายส่วนค้นหา รายการวิดีโอ และการเลือกวิดีโอเพื่อวิเคราะห์')

s=page('หน้าจอจริง: อ่านภาพรวมความรู้สึก','09 / DEMO · ผลวิเคราะห์')
photo(s,'visual-charts.png',.7,2.15,11.95,4.12)
ribbon(s,'ซ้าย: ความรู้สึกบวก / กลาง / ลบ     ขวา: อารมณ์หลักของผู้ชม')
note(s,'ภาพตัดจาก analysis.png ในโปรเจกต์ กราฟซ้ายแสดง sentiment และด้านขวาแสดง emotion ผลในภาพคำนวณจากตัวอย่าง 27 ความคิดเห็น เป็นภาพสาธิตการทำงาน ไม่ใช่ผลประเมินความแม่นยำ')

s=page('ตัวอย่างผลจาก 27 ความคิดเห็น','10 / ผลลัพธ์สาธิต')
for i,(v,t,c,f) in enumerate([('51.9%','เชิงบวก',TEAL,MINT),('14.8%','เป็นกลาง',MUTED,GRAY),('33.3%','เชิงลบ','DA5270',CREAM)]):
    bg(s,.7+i*4.1,2.4,3.75,2.4,f)
    text(s,v,1+i*4.1,2.8,3.15,.85,40,True,c)
    text(s,t,1+i*4.1,3.9,3.15,.55,22,True)
x=.75
for frac,c in [(.519,TEAL),(.148,'A1ACBE'),(.333,'DA5270')]:
    box(s,x,5.3,11.8*frac,.38,c); x+=11.8*frac
ribbon(s,'ตัวอย่างจากหนึ่งวิดีโอ • ไม่ใช่ความแม่นยำของโมเดลหรือความเห็นของผู้ชมทั้งหมด')
note(s,'ที่มา presentation/evidence.json บันทึก 27 กันยายน 2569 วิดีโอจาก T Sports 7 จำนวนตัวอย่าง 27 รายการ สัดส่วน 51.9, 14.8, 33.3 เปอร์เซ็นต์ตามผลระบบ ห้ามตีความเป็นค่าความแม่นยำ หรือสรุปแทนกลุ่มผู้ชมทั้งหมด')

s=page('สิ่งที่ยังต้องระวังในการตีความ','11 / ข้อจำกัด')
for i,(a,b) in enumerate([('ขอบเขตข้อมูล','ตัวอย่างความคิดเห็นหลัก\nไม่ครอบคลุมผู้ชมทั้งหมด'),('ความหมายของภาษา','คำประชด มุก และศัพท์กีฬา\nอาจตีความคลาดเคลื่อน'),('บริการภายนอก','ขึ้นกับโควตา เครือข่าย\nและการตอบกลับของ API')]):
    card(s,.7+i*4.1,2.5,3.75,3.0,a,b,[CREAM,GRAY,MINT][i])
ribbon(s,'ใช้ผลวิเคราะห์เป็นจุดเริ่มต้นในการสำรวจ แล้วอ่านบริบทประกอบ')
note(s,'ไม่รวมทุก reply และไม่ใช่การสุ่มตัวอย่างแทนประชากร ยังไม่มีผลประเมินกับชุดข้อมูลที่มนุษย์ติดป้ายกำกับ ความถูกต้องของโครงสร้างข้อมูลแยกจากความถูกต้องด้านการตีความภาษา')

s=page('ก้าวต่อไป: วัดคุณภาพและทดสอบกับผู้ใช้','12 / ROADMAP')
for i,(a,b) in enumerate([('สร้างชุดอ้างอิง','ให้คนติดป้ายกำกับ\nและตรวจความสอดคล้อง'),('ประเมินโมเดล','Macro-F1\nConfusion matrix'),('ทดสอบใช้งาน','เวลารอผล\nความเข้าใจของผู้ใช้')]):
    card(s,.75+i*4.12,2.5,3.6,3.2,a,b,MINT if i==2 else CREAM,str(i+1))
    if i<2: arrow(s,4.51+i*4.12,3.9,.27,.27,ORANGE)
note(s,'ทั้งหมดเป็นแผนพัฒนาต่อ ไม่ใช่ผลการประเมินที่ทำแล้ว ควรจัดชุดอ้างอิงให้ครอบคลุมบริบทกีฬาและภาษา ใช้ผู้ประเมินมากกว่าหนึ่งคน วิเคราะห์ข้อผิดพลาด และประเมินประสบการณ์การใช้งานจริง')

s=page('จากคอมเมนต์ → สู่ความเข้าใจผู้ชม','13 / สรุป',True)
box(s,0,0,.13,7.5,ORANGE)
for i,(a,b) in enumerate([('ปัญหา','ข้อความมาก อ่านภาพรวมยาก'),('วิธีทำ','YouTube + Gemini + Dashboard'),('คุณค่า','สำรวจเสียงแฟนกีฬาได้ง่ายขึ้น')]):
    text(s,a,.8+i*4.1,2.6,3.7,.55,20,True,'F5B678')
    text(s,b,.8+i*4.1,3.35,3.7,1,18,False,'DCE3EC')
text(s,'ขอบคุณครับ / ค่ะ',.8,5.1,11,1,40,True,WHITE)
note(s,'สรุปว่าโครงงานช่วยจัดกลุ่มและแสดงภาพรวมความคิดเห็นให้สำรวจต่อได้ เปิดช่วงคำถาม แหล่งเนื้อหา: README.md, presentation/evidence.json และภาพใน presentation/assets รูปแบบอ้างอิงจาก PriceHunter PDF ที่ผู้ใช้ให้ ไม่ได้นำข้อกล่าวอ้างหรือข้อมูลธุรกิจของเอกสารนั้นมาใช้')

output=ROOT/'Sports_Analysis_PriceHunter_Style.pptx'
prs.save(output)
(ROOT/'reference-style-speaker-notes.txt').write_text('\n\n'.join(f'{i:02}\n{n}' for i,n in notes),encoding='utf-8')
issues=[]
for i,s in enumerate(prs.slides,1):
    for sh in s.shapes:
        if sh.left<0 or sh.top<0 or sh.left+sh.width>prs.slide_width+1000 or sh.top+sh.height>prs.slide_height+1000:
            issues.append((i,sh.name))
assert not issues,issues
print(f'{len(prs.slides)} slides created; bounds OK; notes included.')
