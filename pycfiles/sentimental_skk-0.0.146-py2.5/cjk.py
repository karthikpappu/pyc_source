# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sskk/canossa/canossa/termprop/termprop/db/unicode6_2/cjk.py
# Compiled at: 2014-04-25 02:25:24
import re
pattern_fullwidth = re.compile('^[¡¤§¨ª\xad®°-´¶-º¼-¿ÆÐ×ØÞ-áæè-êìíðòó÷-úüþāđēěĦħīı-ĳĸĿ-łńň-ŋōŒœŦŧūǎǐǒǔǖǘǚǜɑɡ˄ˇˉ-ˋˍː˘-˛˝˟Α-ΡΣ-Ωα-ρσ-ωЁА-яёᄀ-ᅟ‐–-‖‘’“”†-•․-‧‰′″‵※‾⁴ⁿ₁-₄€℃℅℉ℓ№℡™ΩÅ⅓⅔⅛-⅞Ⅰ-Ⅻⅰ-ⅹ↉←-↙↸↹⇒⇔⇧∀∂∃∇∈∋∏∑∕√∝-∠∣∥∧-∬∮∴-∷∼∽≈≌≒≠≡≤-≧≪≫≮≯⊂⊃⊆⊇⊕⊙⊥⊿⌒〈〉①-ⓩ⓫-╋═-╳▀-▏▒-▕■□▣-▩▲△▶▷▼▽◀◁◆-◈○◎-◑◢-◥◯★☆☉☎☏☔☕☜☞♀♂♠♡♣-♥♧-♪♬♭♯⚞⚟⚾⚿⛄-⛍⛏-⛡⛣⛨-⛿✽❗❶-❿⭕-⭙⺀-⺙⺛-⻳⼀-⿕⿰-⿻\u3000-〩〮-〾ぁ-ゖ゛-ヿㄅ-ㄭㄱ-ㆎ㆐-ㆺ㇀-㇣ㇰ-㈞㈠-㋾㌀-\u4dbf一-ꒌ꒐-꓆ꥠ-ꥼ豈-舘並-龎︐-︙︰-﹒﹔-﹦﹨-﹫！-｠￠-￦�가-힣\ue000-\uf8ff\ufa6e\ufa6f\ufada]$')
pattern_combining = re.compile('^[̀-ͯ҃-҉֑-ׇֽֿׁׂׅׄ\u0600-\u0604ؐ-ًؚ-ٰٟۖ-\u06dd۟-۪ۤۧۨ-ۭ\u070fܑܰ-݊ަ-ް߫-߳ࠖ-࠙ࠛ-ࠣࠥ-ࠧࠩ-࡙࠭-࡛ࣤ-ࣾऀ-ंऺ़ु-ै्॑-ॗॢॣঁ়ু-ৄ্ৢৣਁਂ਼ੁੂੇੈੋ-੍ੑੰੱੵઁં઼ુ-ૅેૈ્ૢૣଁ଼ିୁ-ୄ୍ୖୢୣஂீ்ా-ీె-ైొ-్ౕౖౢౣ಼ಿೆೌ್ೢೣു-ൄ്ൢൣ්ි-ුූัิ-ฺ็-๎ັິ-ູົຼ່-ໍཱ༹༘༙༵༷-ཾྀ-྄྆྇ྍ-ྗྙ-ྼ࿆ိ-ူဲ-့္်ွှၘၙၞ-ၠၱ-ၴႂႅႆႍႝᅠ-ᇿ፝-፟ᜒ-᜔ᜲ-᜴ᝒᝓᝲᝳ឴឵ិ-ួំ៉-៓៝᠋-᠍ᢩᤠ-ᤢᤧᤨᤲ᤹-᤻ᨘᨗᩖᩘ-ᩞ᩠ᩢᩥ-ᩬᩳ-᩿᩼ᬀ-ᬃ᬴ᬶ-ᬺᬼᭂ᭫-᭳ᮀᮁᮢ-ᮥᮨᮩ᯦᮫ᯨᯩᯭᯯ-ᯱᰬ-ᰳᰶ᰷᳐-᳔᳒-᳢᳠-᳨᳭᳴᷀-ᷦ᷼-᷿\u200b-\u200f\u202a-\u202e\u2060-\u2064\u206a-\u206f⃐-⃰⳯-⵿⳱ⷠ-〪ⷿ-゙゚〭꙯-꙲ꙴ-꙽ꚟ꛰꛱ꠂ꠆ꠋꠥꠦ꣄꣠-꣱ꤦ-꤭ꥇ-ꥑꦀ-ꦂ꦳ꦶ-ꦹꦼꨩ-ꨮꨱꨲꨵꨶꩃꩌꪰꪲ-ꪴꪷꪸꪾ꪿꫁ꫬꫭ꫶ꯥꯨ꯭ﬞ︀-️︠-︦\ufeff\ufff9]$')