import configparser

event_template="""
  <div class="center">
    <h2>%%event_title%%</h2>
    <p>%%event_text%%</p>
  </div>
"""

languages = {
  'francais':'index.html',
  'english':'index.en.html',
}

tags = [
  'meta_desc',
  'lang_url',
  'lang_text',
  'intro_title',
  'intro_text',
  'discord_title',
  'discord_text',
  'instagram_title',
  'instagram_text',
  'meeting_title',
  'meeting_text',
]

#
def parse_events(lang: str) -> str:
  cfg_event = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
  cfg_event.read('events.conf')

  event_html = ''  
  for id in range(1,15):
    if cfg_event.has_option(lang, f'event_{id}_title'):
      ev = event_template.replace('%%event_title%%', cfg_event.get(lang, f'event_{id}_title'))
      ev = ev.replace('%%event_text%%', cfg_event.get(lang, f'event_{id}_text').replace('\n', ' '))
      event_html += ev
  return event_html

####
#

# index file template
index_template=''
with open('index.template') as f:
  index_template = f.read()
 
# config file for the basic text  
cfg_text = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
cfg_text.read('text.conf') 
  
  
for lang in languages.keys():
  events = parse_events(lang)
  index = index_template.replace('%%events%%', events)
  for tag in tags:
    index = index.replace(f'%%{tag}%%', cfg_text.get(lang, tag).replace('\n', ' '))
  with open(f'../docs/{languages[lang]}', 'wt') as f:
    f.write(index)
    