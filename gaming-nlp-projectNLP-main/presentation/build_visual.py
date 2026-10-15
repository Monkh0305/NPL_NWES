"""Concise image-led presentation; preserves the original presentation."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
source = (ROOT / 'build_slides.py').read_text(encoding='utf-8')
exec(source.split('# 01 — cover')[0])
prs.core_properties.title = 'อ่านเสียงแฟนกีฬา ด้วย AI'
prs.core_properties.subject = 'สไลด์เน้นภาพสำหรับนำเสนอโครงงาน'

im = Image.open(ROOT/'assets/analysis.png')
w,h=im.size
im.crop((int(w*.065), int(h*.405), int(w*.93), int(h*.875))).save(ROOT/'assets/visual-charts.png')

def page(title, section, dark=False):
    return slide(title,section,dark=dark)

def tile(s,x,y,w,title,subtitle,col=PURPLE):
    box(s,x,y,w,2.1,WHITE,radius=True)
    text(s,title,x+.2,y+.35,w-.4,.65,29,True,col,PP_ALIGN.CENTER)
    text(s,subtitle,x+.2,y+1.15,w-.4,.6,18,False,MUTED,PP_ALIGN.CENTER)

s=page('','SPORTS × NLP',True)
text(s,'อ่านเสียงแฟนกีฬา\nด้วย AI',.75,1.5,5.7,1.9,44,True,WHITE)
text(s,'วิเคราะห์ความคิดเห็นบน YouTube',.8,3.8,5.3,.7,23,False,'C9D3E5')
label(s,'YouTube  →  Gemini  →  Dashboard',.8,5.25,5.2)
photo(s,'analysis.png',6.6,1.35,6.1,4.9)
note(s,'โครงงานเว็บวิเคราะห์ความคิดเห็นต่อวิดีโอกีฬาบน YouTube ใช้ Gemini จำแนกความรู้สึก อารมณ์ และประเด็นที่ผู้ชมกล่าวถึง ภาพเป็นหน้าจอที่บันทึกไว้ในโปรเจกต์เมื่อ 27 กันยายน 2569')

s=page('คอมเมนต์มากมาย… กำลังบอกอะไรเรา?','01 / WHY')
for i,(t,c) in enumerate([('เล่นได้ยอดเยี่ยม!',TEAL),('ทำไมเปลี่ยนตัวตอนนี้?',PURPLE),('เสียดายโอกาสมาก',RED)]):
    box(s,.85,2.3+i*1.15,6.0,.82,WHITE,radius=True)
    text(s,t,1.15,2.43+i*1.15,5.4,.55,25,True,c)
arrow(s,7.3,3.4,.7,.65)
text(s,'เห็นภาพรวม\nในหน้าจอเดียว',8.5,2.85,4,1.8,34,True)
text(s,'ข้อความตัวอย่างประกอบแนวคิด',.9,6.3,6,.3,12,False,MUTED)
note(s,'ข้อความในหน้านี้เป็นตัวอย่างสมมติ ไม่ใช่ข้อความที่ดึงจากวิดีโอ ปัญหาคือการอ่านทีละความคิดเห็นทำให้เห็นภาพรวมได้ยาก ระบบจึงช่วยจัดกลุ่มและสรุปให้สำรวจต่อได้')

s=page('จากวิดีโอ → สู่ความเข้าใจผู้ชม','02 / WORKFLOW')
for i,(a,b) in enumerate([('YouTube','เลือกวิดีโอกีฬา'),('Comments','ดึงความคิดเห็น'),('Gemini','วิเคราะห์ข้อความ'),('Dashboard','แสดงภาพรวม')]):
    tile(s,.7+i*3.2,2.8,2.6,a,b,TEAL if i==3 else PURPLE)
    if i<3: arrow(s,3.45+i*3.2,3.55,.35,.35)
note(s,'ระบบค้นหาวิดีโอหมวด Sports ผ่าน YouTube API แล้วดึงความคิดเห็นหลัก ส่งข้อความตัวอย่างให้ Gemini และตรวจสอบข้อมูลก่อนบันทึกและแสดงผล ค่าเริ่มต้นวิเคราะห์ไม่เกิน 100 ความคิดเห็นต่อรอบ ไม่รวมทุก reply')

s=page('เลือกคลิปที่อยากรู้เสียงตอบรับ','03 / EXPLORE')
photo(s,'dashboard.png',.75,2.0,9.5,4.65)
text(s,'ค้นหา\nเลือกคลิป\nวิเคราะห์',10.5,3.05,2.3,2.4,27,True,PURPLE)
note(s,'ภาพหน้าจอจริงที่จัดเก็บไว้ในโฟลเดอร์ assets แสดงการค้นหาและเลือกวิดีโอ ผู้ใช้เลือกคลิปแล้วเรียกการวิเคราะห์ ภาพนี้เป็นภาพบันทึก ไม่ใช่ข้อมูลสดขณะนำเสนอ')

s=page('ความรู้สึกและอารมณ์ เห็นได้ในภาพเดียว','04 / DASHBOARD')
photo(s,'visual-charts.png',.65,2.1,12,4.35)
note(s,'กราฟซ้ายแสดงสัดส่วน sentiment ส่วนกราฟขวาแสดงอารมณ์หลัก ผลจากภาพตัวอย่างมี 27 ความคิดเห็น ใช้เพื่อสาธิตการแสดงผล ไม่ใช่ผลประเมินความแม่นยำของโมเดล')

s=page('ตัวอย่าง 27 ความคิดเห็น','05 / SAMPLE')
vals=[('51.9%','เชิงบวก',TEAL),('14.8%','เป็นกลาง','94A3B8'),('33.3%','เชิงลบ',RED)]
x=.8
for value,caption,col in vals:
    tile(s,x,2.4,3.75,value,caption,col); x+=4
x=.85
for fraction,col in [(0.519,TEAL),(.148,'94A3B8'),(.333,RED)]:
    box(s,x,5.05,11.6*fraction,.5,col); x+=11.6*fraction
text(s,'ผลสาธิตจากหนึ่งวิดีโอ • ไม่ใช่ตัวแทนผู้ชมทั้งหมด',.85,6.0,11.7,.5,19,False,MUTED)
note(s,'อ้างอิง presentation/evidence.json และภาพ analysis.png ที่บันทึกในโปรเจกต์ ตัวอย่างวิดีโอจาก T Sports 7 บันทึกวันที่ 27 กันยายน 2569 เชิงบวก 51.9 เปอร์เซ็นต์ เป็นกลาง 14.8 เปอร์เซ็นต์ และเชิงลบ 33.3 เปอร์เซ็นต์ ตัวเลขนี้เป็นผลจำแนกของระบบ ไม่ใช่ความแม่นยำและไม่ควรสรุปแทนผู้ชมทั้งหมด')

s=page('มากกว่าความรู้สึกบวกหรือลบ','06 / INSIGHTS')
for i,(a,b) in enumerate([('อารมณ์','ผู้ชมรู้สึกอย่างไร'),('ประเด็น','ผู้ชมพูดถึงอะไร'),('สรุปไทย','จับใจความสำคัญ')]):
    tile(s,.8+i*4.15,2.65,3.8,a,b,[TEAL,PURPLE,RED][i])
text(s,'ความรู้สึก  •  อารมณ์  •  หัวข้อ  •  คำสำคัญ',1,5.7,11.3,.65,24,True,INK,PP_ALIGN.CENTER)
note(s,'Gemini ส่งผลแบบ structured JSON ครอบคลุม sentiment, emotion, topics, keywords และสรุปภาษาไทย หนึ่งความคิดเห็นอาจมีหลายประเด็น สัดส่วนหัวข้อจึงอาจรวมเกิน 100 เปอร์เซ็นต์ จำนวนคำสำคัญนับจากความคิดเห็นจริงตามวิธีในระบบ')

s=page('เบื้องหลังหน้าจอเดียว','07 / ARCHITECTURE')
for i,(a,b) in enumerate([('React','ส่วนติดต่อผู้ใช้'),('FastAPI','ตรวจสอบและคำนวณ'),('Gemini API','วิเคราะห์ภาษา')]):
    tile(s,.85+i*4.15,2.45,3.55,a,b)
    if i<2: arrow(s,4.52+i*4.15,3.25,.35,.35)
label(s,'YouTube API · แหล่งความคิดเห็น',4.65,5.2,4.1)
label(s,'SQLite · จัดเก็บผลวิเคราะห์',4.65,5.85,4.1)
note(s,'React และ Vite เป็น frontend ส่วน FastAPI ประสาน YouTube API และ Gemini API ตรวจสอบคำตอบก่อนคำนวณและจัดเก็บด้วย SQLite คีย์ API อยู่ฝั่ง backend ระบบไม่โหลดโมเดลมารันในเครื่อง อ้างอิง README.md และซอร์สโค้ดของโปรเจกต์')

s=page('อ่านผลอย่างเข้าใจขอบเขต','08 / LIMITS')
for i,(a,b) in enumerate([('ตัวอย่าง','ไม่ใช่ผู้ชมทั้งหมด'),('บริบท','มุก / ประชด / ศัพท์กีฬา'),('ขั้นต่อไป','ประเมินเทียบคนจริง')]):
    tile(s,.8+i*4.15,2.65,3.8,a,b,[TEAL,PURPLE,RED][i])
note(s,'ข้อมูลเป็นตัวอย่างความคิดเห็นหลักสูงสุดตามค่าตั้งต้น 100 รายการ ไม่ใช่การสุ่มแทนผู้ชมทั้งหมด โมเดลอาจตีความคำประชดหรือศัพท์กีฬาไม่ตรงบริบท ยังไม่มีผลประเมินความแม่นยำกับชุดข้อมูลที่มนุษย์ติดป้ายกำกับ แผนต่อไปคือสร้างชุดอ้างอิง ประเมิน Macro-F1 และทดสอบการใช้งาน')

s=page('','DISCUSSION',True)
text(s,'จากเสียงแฟนกีฬา\nสู่ภาพรวมที่เข้าใจง่าย',.9,1.75,11.8,1.9,43,True,WHITE)
text(s,'YouTube  →  AI  →  Insight',.95,4.15,11,.8,29,True,'A99BFF')
text(s,'คำถามและข้อเสนอแนะ',.95,5.75,11,.7,26,False,'C9D3E5')
note(s,'ปิดการนำเสนอด้วยคุณค่าของโครงงาน คือช่วยสำรวจความคิดเห็นและสื่อสารภาพรวมได้ง่ายขึ้น เปิดให้ถามเรื่องขอบเขตข้อมูล การตรวจสอบคำตอบ และแผนประเมินคุณภาพ แหล่งข้อมูลของสไลด์: README.md, presentation/evidence.json และภาพหน้าจอใน presentation/assets รายละเอียดภาพและข้อจำกัดอยู่ในโน้ตแต่ละหน้า')

output=ROOT/'Sports_Analysis_Visual.pptx'
prs.save(output)
(ROOT/'visual-speaker-notes.txt').write_text('\n\n'.join(f'{i:02d}\n{n}' for i,n in notes),encoding='utf-8')
issues=[]
for i,s in enumerate(prs.slides,1):
    for sh in s.shapes:
        if sh.left<0 or sh.top<0 or sh.left+sh.width>prs.slide_width+1000 or sh.top+sh.height>prs.slide_height+1000:
            issues.append((i,sh.name))
assert not issues, issues
print(f'Created {output.name}: {len(prs.slides)} slides, speaker notes on every slide, bounds OK')
