from django import template


register = template.Library()
bad_words = [
   'редиска',
   'жмот',
   'чебурашка',
]


@register.filter()
def censor(value):
   nvalue = str(value)
   nvalue = nvalue.split()
   for i in range(len(nvalue)):
      word = nvalue[i].lower()
      if word in bad_words:
         nvalue[i] = (nvalue[i][0] + '*'*(len(nvalue[i])-1))
   return ' '.join(nvalue)
