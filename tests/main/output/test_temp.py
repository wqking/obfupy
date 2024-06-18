from functools import wraps
(lllIllI1ll1I, III11l11l1ll, l1111llIIIll, IIlllII111Il, ll111lIlll1l, Illll1111IIl, lII1lIlII111, lll11IIII11I, llII1lIll1ll, lIlII1I111ll, I1IIIlI1llll, ll11IllI1lII, l11l1II1ll1l, I1Il1l1ll1lI, I1II11lII11l, l11II1I11I1l, IIlI1IIIl1II, II11lIlI111I, lIII1II1IIlI, lIllIIlIIIll, III1l1l111ll, IIlII11I11ll, IIII1l1lIIlI, II1I1lI111ll, l1llIIllIl11, llIlIll1l1ll, l11IIIlIl11I, llIlI11111ll, l1lIIl1Il1ll, IIllll1llI11, IIllll1I11I1, II1llIl1I1II, Il11IIIlII1l, III1l11l11Il, I1I1Il1ll1ll, IIlI1l1lIIII, IIllI111I1lI, I11II11Il1II, I1lIII1I1Il1, l11I1lIlIIlI, lllI11I1I1II, II11IlIIIl1I, II1lIII1IlI1, l1l11Il1lIll, IlllI1I11I1l, ll11lIlI1I1I, IlIIl1IIlIl1, IlIl1IIllII1, lIl1I11l1l1l, Il1IIl1l1lll, l1llll1lllII, IlIllllIIIIl, lIIIl11III1I, l1Il1ll11I1l, ll1I111Il1l1, l1lllI11I1Il, lI11ll1Il1lI, l1l1lllIl1lI, IIl11lllIIlI, lI11III1IIl1, l11lll1Il1II, I1l11IIIlIl1, lI11III11ll1, lIIlllIIIII1, IIIlI11llIIl, l1lIl1ll1I1I, lll1l11I11lI, lIII1lII11lI, lIIII1IIIIII, IIlIll1lI1Il, l11lI1l1I1Il, l1llII1I1III, l11llllIl1II, Il11I11l111l, IllII1lll1II, l111Il1IlIl1, I11l1lIIlI1I, Illll11l11ll, Ill1Il1l11lI, Il1IIllI1III, lIIl1IlIlI1I, II111lI11l1l, I111l1lllIl1, ll11IIl11Ill, lI11I11IIll1, IIlIIIlII1II, II1llI1II1II, l11II1II11II, lII1l1I1Il1l, lI1IlIlI1Ill, IIl1IIll11ll, I1l1111111l1, ll1lllIII1lI, l1I1lI1Illl1, III1l11ll1II, IIII11I111l1, lI1ll11lIlll, I11l1II1ll11, l1l1I111l11l, llIlIl1I1l1l, l1lll1lIl11I, IllIl11IIIll, lI1I111lIIIl, IlI11l1Il1II, I111lIll1lll, III1II1I11II, II1IIIl111l1, lII1II111lII, I1I1I111I11l, I11IIlIlllll, IlIII11IlI1I, IIIIl1lIIl11, lIlIIlllII1I, lI1l1I111Il1, lIII11l11l1l, l1I11IlllIIl, Il11I1ll1III, l1Il1lII11Il, lIl1lIlI1lI1, llI11IlllI1l, l11llll1l1I1, l1111ll1lI1I, ll11Ill1IlI1, I1Il1IIII1lI, lI1lIl1l1l1l, Il11IlllIl1I, lI11I111lI1I, II1I1Ill11ll, II1lII111Ill, l1IlI1llI1I1, II1lI1Il1lII, lI1llllI11I1, lI1llIllI1l1, I1lI11l11l11, lIlIll1lll11, l1l1I1l11111, IlI11lI11Ill, IlI1lII1IllI, lI1llIllIlll, I11I1lIl1llI, III1IlI1I1lI, lIl111lIl1ll, I1I1I11lll11, lIIl1I1I1IlI, l1lIIll11lIl, Il11IIIIl1II, Il1IIIIl1I11, IlIllIIIIIIl, llIlll1l1I1l, I1I11lI1lllI, lII1IIII1I1I, IIl1Ill111Il, lI11lI11lll1, lIll111III11, llIIIlllI111, lll1II1I1I11, IIl1IlllI1II, I11lI1lll1I1, l11lll1l11lI, lIIIl1lllI1l, lll1ll1lllI1, IlIII1111ll1, I1ll1l1lIlIl, I1II1lI1IllI, I1l1II1l1l1l, I1I1ll1IIlIl, IlIIl1l11l11, IlI11l11III1, llll1lIlI1ll, llllI1Ill111, l1Ill1lIl1I1, lI1IIlII111I, lI11ll1111lI, IllIl111111I, lll1I1lII1lI, ll1lIlll1IlI, IlIII1lI1lIl, llIll1Il1II1, Il1I11III1ll, lIl1llIl11II, lIlIlI1I1I1I, lll11Il1lllI, llIII1I11lll, Il1lIIll11l1, l11lllll1I11, IIIII1I11I1I, IIIIl1Il1III, Il111l111I11, lI1Ill1l1I1l, ll1IllII1llI, l1I1lI111Il1, lIIllI1IIl1l, I1l1ll111Il1, ll1lll1l1lII, II11lll1I1lI, Il1IIII1lI1I, ll11I1111lIl, II1l1llIlll1, IlIII1l11I1l, lIl1l1I111lI, ll1l11l1lIlI, l11IIlII1I11, Il11llIllll1, IIllIl1IllII, lIIlI1lllII1, Il11l1l11Ill, Il11l1l1l11l, ll1ll1lI1IIl, l11l1lI1ll1l, I111l1lIIl1I, l1lIl1IIIllI, ll1lII111IIl, lI1lI1I11I11, I11lI11II1I1, ll1l11IIIIl1, IlIIll1lIIll, II1I1I11llll, I1ll1I1lI1l1, l11IlIll111I, Il11l11IIIII, I1lI1l1I111l, I1l1I111I111, II1IlI11Il1I, Ill1l111Illl, l1llI1I1IlI1, II11lIIlll1l, lIIll111lII1, III111III1I1, I1I1lll1Il11, lll1ll1111ll, llI1l1IIIlll, I11IlI11Ill1, I1llIIllII1I, lI1I11lIIIII, lIlllIIIlI1I, Il1l1lIIIIl1, lII1Il1IlIl1, lIIIlIIlI11l, III111I11111, IlIIlll1llIl, l1lllIIIl11l, l1II1lll1I1I, IIll1lllllIl, l11I1ll1III1, II11II11lI1l, II1IlII1II1I, IIIlIl11lll1, l1IllIlIIl1I, Il1lI11II1II, lllIl11lIlII, I1lIl1llIIll, llll1l1IlI1I, l1l1lI11I11l, l1lIIll11lI1, lI1Il1lIlIl1, lIllIlI1111l, I1IlII1l111l, I1lI111111lI, Il1lI11l1Il1, I1II111111Il, IIII1lI1l1l1) = (~-884617450 ^ ~-884617412, ~-636386792 ^ (512284797 ^ 996582787), ~(445871599 - 445871614), setattr, 380783644 ^ 980593806 ^ ~-750837900, 971178414 - 626543335 ^ 872277751 + -527642643, 12407559 + 118380573 - (468741207 ^ 473679697), ~-560133355 ^ (851984512 ^ 329954428), ~(275884899 + -275884922), ~-842874781 ^ ~-842874815, 87885215 + 703143100 ^ (339619420 ^ 991431714), 363764216 ^ 522425000 ^ 730240301 + -553224680, ~-983150833 ^ ~-983150845, ~-(695431036 ^ 695431006), ~(735983508 + -735983556), 591522929 + 344695407 - (630721927 + 305496402), 410457233 + -149954861 ^ (909675003 ^ 968784520), 464003234 + -370496877 + -~-93506313, 554758518 ^ 187391662 ^ ~-708554690, (910953586 ^ 1038296814) + -(513873938 ^ 353251987), 93665588 ^ 1010988456 ^ 677526112 - -292885040, 478754581 - 262982099 - (50168922 ^ 237103470), (530038307 ^ 823140578) + -(789255787 ^ 25987292), (393580302 ^ 827448974) - (400044139 ^ 838623497), ~-267060649 ^ 415034175 + -147973560, ~-(472136775 ^ 472136769), 286480509 ^ 61051203 ^ (18536576 ^ 329912764), 61058714 ^ 120975530 ^ (288172776 ^ 364606671), 309867599 ^ 726993113 ^ (515844486 ^ 663885080), (467195842 ^ 850637666) - (946954133 - 252050181), 798121356 ^ 580841416 ^ 878314525 - 659378605, 666917086 - 348184404 ^ (29006274 ^ 323346523), 812371714 ^ 933723036 ^ (719337691 ^ 757894223), ~-(377836637 ^ 377836568), 557194084 - 254313155 ^ 354441533 + -51560601, 103137290 ^ 421061513 ^ (110673297 ^ 430284336), 727418970 + -53571669 ^ ~-673847341, ~(403628820 - 403628860), 551376127 + -469207146 ^ (195196401 ^ 256358724), id, 807911169 + 132950547 + (952436132 - 1893297807), ~(849995547 - 849995591), ~-368133710 ^ 492378265 - 124244542, (73770650 ^ 425026386) + -(844776938 ^ 795508876), ~-909954914 - (767020315 ^ 462094892), range, 798588338 - 512258772 ^ 136536497 - -149793039, format, (561248310 ^ 1003108296) - (273458142 ^ 183856163), 91652835 + -15538332 ^ 443835034 - 367720500, (532218194 ^ 418317493) - (393321560 ^ 271030676), 290430044 - -231705401 ^ 9783250 + 512352176, ~(396733563 + -396733613), 376832272 - -359363051 ^ 577336912 + 158858388, ~-~-55, 122704947 ^ 137609939 ^ 639716574 + -381531663, 823184694 ^ 765383009 ^ (323517741 ^ 264659301), 203762713 - -253905059 ^ 808604684 - 350936948, ~-(718732425 ^ 718732454), (452468256 ^ 262493067) - (574730553 ^ 924646579), (682526315 ^ 552106179) - ~-138870437, 115331100 + 806450362 + -(99839959 ^ 855780208), (685515439 ^ 168145368) + (422023106 - 1006707500), 164404124 ^ 298508836 ^ (229021410 ^ 362868596), 406067844 + 259256016 ^ (368929874 ^ 844457217), 371489276 ^ 384775498 ^ 259608121 - 246284671, (940350200 ^ 417795419) + -~-552310659, 25069139 + 11652361 ^ (959618143 ^ 990039840), 311473271 ^ 296069228 ^ ~-53812249, ~-(785502125 ^ 785502121), ~-179849706 ^ (898235175 ^ 1060221670), ~-301994482 + -(509261416 ^ 207267754), (443609441 ^ 867383778) - ~-700696691, 446779979 + -314503990 ^ (926915826 ^ 819839974), 408457098 ^ 492695658 ^ 875940762 - 791694240, ~-(817684068 ^ 817684086), 790540303 - 67825655 - ~-722714611, ~-(128571173 ^ 128571192), ~(834923813 - 834923829), (238897204 ^ 443924641) + (780233364 + -1120531230), 936279303 - 519923769 ^ 718947430 - 302591969, 782593482 - 485488808 ^ (992097247 ^ 714557119), 608427648 - 218798240 ^ (37760901 ^ 360278601), 452780622 + -20018563 ^ (835515727 ^ 671586714), (112912619 ^ 702683849) + -(141637773 ^ 657049979), 802265649 - -115577522 ^ (496370480 ^ 723726327), 444090254 ^ 529323411 ^ (774565169 ^ 736001842), 414679911 - -48515252 ^ 251302814 - -211892376, (414979002 ^ 42792107) + (152991880 - 592404343), (575521440 ^ 74308977) + (591069177 + -1230708656), 817130287 + 181212406 + -(378109291 ^ 755563883), 418346187 - -288758611 ^ (881478705 ^ 514841644), 397213073 + 103913458 - (974787317 + -473660793), 923756447 - 721357725 - (528762751 + -326364073), 170262403 - -735790488 + (430078401 - 1336131289), ~-874215880 ^ ~-874215919, (504532546 ^ 192434687) + (642413030 + -1001738639), ~-(423737579 ^ 423737599), (319587575 ^ 78087043) + -(852359772 ^ 627506540), ~-(282742984 ^ 282742930), ~-(929381511 ^ 929381523), ~-(336720927 ^ 336720904), ~-(919023653 ^ 919023617), ~(250193876 - 250193911), 44433877 - -364381918 ^ (3230519 ^ 409944986), (708351438 ^ 509331926) - (40664253 - -838262608), 101426717 ^ 219480009 ^ (701435316 ^ 584078450), 532443800 - -256597840 - (922327582 - 133285980), (228937578 ^ 987085639) + -(875081327 ^ 56121922), 225639511 ^ 673105487 ^ 208771337 - -419078439, (494857777 ^ 1045472722) - (921500443 ^ 365080736), ~-~-40, 986018071 ^ 249262396 ^ (545546662 ^ 345661935), 8790284 + 710756211 + (323437122 - 1042983579), 25571801 ^ 763257121 ^ 596511975 + 157959149, 622658049 ^ 319534431 ^ 186045573 - -721412814, 689706997 ^ 85964177 ^ 332677751 + 405757956, ~-317380304 ^ 195724831 - -121655475, ~-778470901 ^ 44928334 - -733542558, ~(83139882 - 83139920), 427739097 ^ 1017602858 ^ 972792633 + -337772136, ~-(700889282 ^ 700889304), 202719614 ^ 88344766 ^ ~-156322260, ~-(790785901 ^ 790785859), ~-~-44, 450487108 + 148010769 ^ (907534765 ^ 364624891), 633237421 ^ 693189561 ^ 753459615 - 536448396, 816714970 - 534576972 ^ (446347273 ^ 172731784), isinstance, 96591364 + 286859173 - (830791424 ^ 660480645), 500129592 - -431540499 - (594293399 + 337376643), (263715706 ^ 740849176) - (235444965 - -362213965), ~(830478102 + -830478135), str, 603002245 ^ 6905549 ^ (894241372 ^ 383074598), (72107592 ^ 1012432381) + -(456908175 ^ 590341664), 809560634 - 412279194 ^ (505646294 ^ 160269397), ~-405791696 + -~-405791694, 504972740 - -425129279 ^ ~-930102032, ~-297800823 ^ (682534010 ^ 963555388), ~-140479026 - (835874408 + -695395414), 994708621 + -720083255 ^ (828541944 ^ 557643963), ~-(600957994 ^ 600957956), 455190553 ^ 354816385 ^ (113333123 ^ 147253763), 641271773 ^ 298763618 ^ (802937981 ^ 405544683), 264417390 + -208188231 + (36062015 + -92291132), 335204605 + 191989320 ^ (204187225 ^ 323481876), 105521167 + 872215519 + -(779071976 ^ 338207245), 704749296 ^ 64474563 ^ 362687230 - -339224622, (941216721 ^ 541050675) - (402054208 ^ 265341078), ~-(6512977 ^ 6512986), 661003514 ^ 141235469 ^ (862800905 ^ 476071387), ~-376291943 ^ (514449286 ^ 147070443), 370742097 ^ 200481464 ^ ~-501877153, (269280172 ^ 397802806) + -~-129572424, 72011120 ^ 853307710 ^ 268748327 + 647099947, ~-621563156 ^ ~-621563139, (36724610 ^ 840053057) + -(865589985 ^ 62239835), 505403725 ^ 10457196 ^ (254357192 ^ 296314872), 818341948 ^ 487915105 ^ (895213278 ^ 411682995), (4332325 ^ 134054306) - (277512190 - 147514776), 158388743 ^ 591689494 ^ (887245024 ^ 517402005), 369080636 ^ 958881947 ^ 255717197 - -496691769, isinstance, ~-(726203695 ^ 726203702), repr, 544403896 + -338229248 ^ 873567481 - 667392852, ~-~-25, ~-(454256357 ^ 454256348), 569508167 - 413319270 + -(984419616 ^ 870469089), range, 484319351 ^ 145696646 ^ (697927704 ^ 1038651333), hasattr, getattr, ~-438830142 ^ 845363356 + -406533225, ~-338088233 ^ (482631611 ^ 149065395), 790080769 ^ 175121057 ^ (428965040 ^ 1022817049), 91557921 ^ 807090040 ^ 795374643 + 101036821, ~-222210570 ^ (759248511 ^ 545234001), 936133522 + -740313745 + -(398718122 ^ 476580945), 448314938 + -11997221 ^ (103896801 ^ 472971519), 906410174 - 400028831 + -(138860242 ^ 375919317), 686271159 ^ 983299957 ^ (931046935 ^ 620952543), ~-350906828 ^ (275168415 ^ 76338505), ~-595852156 ^ (220929291 ^ 782820967), ~-~-41, (419895603 ^ 592720148) - (295342322 ^ 734640360), 499401231 ^ 730944970 ^ 176625818 - -734920489, (928890278 ^ 615368250) + (204583777 + -539111122), 515070565 + -255170790 ^ 85110957 + 174788769, ~-770484996 - (278696616 ^ 1030764669), ~-(941607949 ^ 941607963), ~-(552428077 ^ 552428041), 859666214 - 629439570 ^ ~-230226644, ~-(921501259 ^ 921501271), (545438962 ^ 162731447) - (277920129 - -413200277), 247988832 ^ 880189878 ^ ~-985572292, 98584529 - 31719741 ^ 850833059 - 783968277, ~-537456731 ^ (782452433 ^ 246134412), 951015546 ^ 141616457 ^ ~-819969335, 'cba'[::-1], hash, None, (822226309 ^ 76717854) - (962057256 ^ 214394555), 81476900 ^ 206483050 ^ (678338451 ^ 553323735), isinstance, ~-661741265 ^ ~-661741281, 457121581 ^ 1066457732 ^ ~-615499195, 599495881 ^ 653860089 ^ (278136476 ^ 366382826), (706549667 ^ 633887069) - (873110447 ^ 1004524877), 182388615 + 8208812 + -(954744678 ^ 867464782), 940617161 ^ 808714930 ^ 194713846 - 58091905, ~(262848581 - 262848595), 165126103 ^ 455122860 ^ 86744179 - -231433165, (932493342 ^ 473761817) - (806174118 ^ 463770195), ~-(108193629 ^ 108193646), 973099306 ^ 986677727 ^ (898616136 ^ 893393837), ~(633648707 + -633648720), ~-570714429 ^ (751809567 ^ 248241463), ~-(526578038 ^ 526578047), 839470444 + 150887228 + -(446073503 ^ 563159575), 140232712 ^ 577663813 ^ (722093218 ^ 20971512), 947917316 - 175509838 ^ (845831313 ^ 476077077), ''.join([chr(I1ll11II11II ^ 30219) for I1ll11II11II in [30314, 30314, 30314]]), 939647854 ^ 546948160 ^ (179342730 ^ 304654980), 323926322 ^ 718882492 ^ ~-966262692, (696594677 ^ 574831847) + (553372059 + -750900649), 364227375 + -157115954 ^ ~-207111400, ~-951745280 - (213599352 - -738145877), 999487518 ^ 227690234 ^ ~-906018534, ~-~-67, 428619975 ^ 872947208 ^ 871498915 + -107863512, ~-(846161517 ^ 846161482), 665653393 ^ 766740393 ^ ~-169777024, ~-535336772 ^ (347940503 ^ 190165452), 781503314 + 30430491 ^ 800511989 - -11421810, 618984935 ^ 334923389 ^ (668769737 ^ 281996921), 320877917 ^ 513610720 ^ ~-230500002, 402045767 + -102793795 ^ 851516850 - 552264869, ~(819235082 + -819235126), ~-518898989 ^ 424032776 - -94866174, ~-269651588 ^ (582223834 ^ 849774912), (758972546 ^ 420122075) - (991697751 + -115641856), ~(350119969 - 350119985), 236490055 + 646155201 ^ (421291284 ^ 763395125), ~-172696339 - (842468172 + -669771879), 691041722 + -310638086 ^ 313090889 + 67312748, (491489786 ^ 883504883) + -(518785836 ^ 923710914), ~-898753825 + -(822292187 ^ 76728870), ~-~-29, ~-143555006 - (435476426 ^ 293252718), 18415447 ^ 739010444 ^ (453527258 ^ 907861543), ~-226466211 ^ ~-226466227, ~-839283955 ^ ~-839283907, (643156753 ^ 942380664) + -~-511597847, ~-(117895345 ^ 117895355), 708937131 ^ 523854314 ^ ~-897115209, 9950376 + 331618891 - (780389542 ^ 987243094), 966032659 ^ 228188079 ^ 365264686 - -508044130, ~-(722689890 ^ 722689828), 251208316 - -331529926 ^ (240174081 ^ 753608002))

def llllIIIllIII(l1llI11l11II):
    return True

def llll1l1Illll(l1llI11l11II):
    return l1llI11l11II

class II111l1111ll:

    @staticmethod
    def ll1lI1l1Il1l(llllIl1lIIII):
        return True

    @staticmethod
    def IIIlII1l111I(llllIl1lIIII):
        return llllIl1lIIII
Il111II11lII = lambda III1l1IIII11: True
IIlIl1I1ll1l = lambda III1l1IIII11: III1l1IIII11

def lII1IIll11l1(II11Il1lllIl, I1ll1Il1IlI1):
    try:
        return II11Il1lllIl != I1ll1Il1IlI1
    except:
        return not II11Il1lllIl == I1ll1Il1IlI1

def lllIII111ll1(ll1lllI1l1ll, lllllIl1l1l1):
    try:
        return ll1lllI1l1ll == lllllIl1l1l1
    except:
        return not ll1lllI1l1ll != lllllIl1l1l1

def l11l11l11l1l(lIIllII1I1I1, l111IllI11l1):
    try:
        return lIIllII1I1I1 >= l111IllI11l1
    except:
        return not lIIllII1I1I1 < l111IllI11l1

def I11I11l1lI1l(Illl1I11IlI1, lll1l11l1l11):
    try:
        return Illl1I11IlI1 > lll1l11l1l11
    except:
        return not Illl1I11IlI1 <= lll1l11l1l11

def IlIlIlI1lII1(II1IIIllII1I, II1l1l1III1l):
    try:
        return II1IIIllII1I <= II1l1l1III1l
    except:
        return not II1IIIllII1I > II1l1l1III1l

def lI1lIIIllII1(Il111lI1III1, ll11I1IIIlIl):
    try:
        return Il111lI1III1 < ll11I1IIIlIl
    except:
        return not Il111lI1III1 >= ll11I1IIIlIl

class Promise:
    """
    Base class for the proxy class created in the closure of the lazy function.
    It's used to recognize promises in code.
    """
    pass

def ll1l1I11ll1l(lI1lIl1I11II_func_5233, *Il1II1ll1I1I_resultclasses_33174):
    """
    Turn any callable into a lazy evaluated callable. result classes or types
    is required -- at least one is needed so that the automatic forcing of
    the lazy evaluation code is triggered. Results are not memoized; the
    function is evaluated on every access.
    """

    class __proxy__(Promise):
        """
        Encapsulate a function call and act as a proxy for methods that are
        called on the result of that function. The function is not evaluated
        until one of the methods on the result is called.
        """

        def __init__(self, args, kw):
            (lllII1II1llI_self_41291, IlII111lIl1I_args_72433, IlIllIIIIl11_kw_21075) = (self, args, kw)
            lllII1II1llI_self_41291._args = IlII111lIl1I_args_72433
            lllII1II1llI_self_41291._kw = IlIllIIIIl11_kw_21075

        def __reduce__(self):
            I1I1IlIlI1lI_self_14835 = self
            return (_lazy_proxy_unpickle, (lI1lIl1I11II_func_5233, I1I1IlIlI1lI_self_14835._args, I1I1IlIlI1lI_self_14835._kw) + Il1II1ll1I1I_resultclasses_33174)

        def __deepcopy__(self, memo):
            (lllll11ll11l_self_33680, llIll1l111l1_memo_49333) = (self, memo)
            llIll1l111l1_memo_49333[l11I1lIlIIlI(lllll11ll11l_self_33680)] = lllll11ll11l_self_33680
            return lllll11ll11l_self_33680

        def __cast(self):
            l1I1III1II1l_self_60410 = self
            return lI1lIl1I11II_func_5233(*l1I1III1II1l_self_60410._args, **l1I1III1II1l_self_60410._kw)

        def __repr__(self):
            lI1111lIl11I_self_60759 = self
            return I1I1ll1IIlIl(lI1111lIl11I_self_60759.__cast())

        def __str__(self):
            l11lIl1IIIIl_self_52303 = self
            return I1lI11l11l11(l11lIl1IIIIl_self_52303.__cast())

        def __eq__(self, other):
            (III11lIl1l1I_self_12415, IIl1llIII1II_other_40526) = (self, other)
            lI1lll1l11II = IlIIl1l11l11
            llll11IlII1I = I1lI111111lI
            if not Il111II11lII(II1lIII1IlI1):
                llll11IlII1I = IIllll1llI11
            else:
                llll11IlII1I = IIlIIIlII1II
            if llll11IlII1I == IIlIIIlII1II:
                if not Il11l1l11Ill(IIl1llIII1II_other_40526, Promise):
                    llll11IlII1I = IIllll1llI11
                else:
                    llll11IlII1I = l1II1lll1I1I
            if llll11IlII1I == II1I1I11llll:
                lI1lll1l11II = I11IlI11Ill1
            if llll11IlII1I == ll111lIlll1l:
                lI1lll1l11II = Il11I1ll1III
            if lI1lll1l11II == lIIll111lII1:
                Il1lllIll1II = II1I1lI111ll
                if not II111l1111ll.ll1lI1l1Il1l(lII1II111lII):
                    Il1lllIll1II = l11llllIl1II
                else:
                    Il1lllIll1II = IlIIlll1llIl
                if Il1lllIll1II == lI1Ill1l1I1l:
                    if not Il111II11lII(llIlll1l1I1l):
                        Il1lllIll1II = I11II11Il1II
                    else:
                        Il1lllIll1II = l11llllIl1II
                if Il1lllIll1II == I11II11Il1II:
                    lI1lll1l11II = Il11I1ll1III
                if Il1lllIll1II == l11llllIl1II:
                    lI1lll1l11II = l1lIIll11lIl
            if lI1lll1l11II == II11II11lI1l:
                pass
            if lI1lll1l11II == Il11I1ll1III:
                IIl1llIII1II_other_40526 = IIl1llIII1II_other_40526.__cast()
            return not lII1IIll11l1(III11lIl1l1I_self_12415.__cast(), IIl1llIII1II_other_40526)

        def __ne__(self, other):
            (ll1lIllI1lII_other_60104, l1llI11IIl1I_self_42444) = (other, self)
            I1lIlIl1lI1l = I1l1II1l1l1l
            IIlIIl1I111I = IIII1lI1l1l1
            if not llllIIIllIII(Il11IlllIl1I):
                IIlIIl1I111I = lll11IIII11I
            else:
                IIlIIl1I111I = IIl1IIll11ll
            if IIlIIl1I111I == IIl1IIll11ll:
                if not llllIIIllIII(IIlIll1lI1Il):
                    IIlIIl1I111I = IllIl11IIIll
                else:
                    IIlIIl1I111I = I11IIlIlllll
            if IIlIIl1I111I == I11IIlIlllll:
                I1lIlIl1lI1l = IlIII1l11I1l
            if IIlIIl1I111I == II1lIII1IlI1:
                I1lIlIl1lI1l = I11IIlIlllll
            if I1lIlIl1lI1l == IlIII1l11I1l:
                l11IlIllIlll = Il1lI11II1II
                if not l11l1II1ll1l:
                    l11IlIllIlll = IlllI1I11I1l
                else:
                    l11IlIllIlll = Il111l111I11
                if l11IlIllIlll == Il111l111I11:
                    if not I1II1lI1IllI(ll1lIllI1lII_other_60104, Promise):
                        l11IlIllIlll = IIlI1l1lIIII
                    else:
                        l11IlIllIlll = Il11IIIIl1II
                if l11IlIllIlll == Il11IIIIl1II:
                    I1lIlIl1lI1l = I111l1lIIl1I
                if l11IlIllIlll == IlI11l1Il1II:
                    I1lIlIl1lI1l = I11IIlIlllll
            if I1lIlIl1lI1l == I11IIlIlllll:
                pass
            if I1lIlIl1lI1l == I111l1lIIl1I:
                ll1lIllI1lII_other_60104 = ll1lIllI1lII_other_60104.__cast()
            return not lllIII111ll1(l1llI11IIl1I_self_42444.__cast(), ll1lIllI1lII_other_60104)

        def __lt__(self, other):
            (IlIll1Ill1I1_other_4854, I111l111l1Il_self_30843) = (other, self)
            I1I1IllIIIl1 = III1IlI1I1lI
            Il11llIl1IlI = IIl1IIll11ll
            if not II1lII111Ill(IlIll1Ill1I1_other_4854, Promise):
                Il11llIl1IlI = IIlI1l1lIIII
            else:
                Il11llIl1IlI = l1lIl1IIIllI
            if Il11llIl1IlI == lIlIlI1I1I1I:
                if not IIlII11I11ll:
                    Il11llIl1IlI = IIlI1l1lIIII
                else:
                    Il11llIl1IlI = l1lllI11I1Il
            if Il11llIl1IlI == IIlI1l1lIIII:
                I1I1IllIIIl1 = IIII1l1lIIlI
            if Il11llIl1IlI == l1lllI11I1Il:
                I1I1IllIIIl1 = IIlII11I11ll
            if I1I1IllIIIl1 == lll1I1lII1lI:
                IIlIII1lIlll = IlIIll1lIIll
                if not II111l1111ll.ll1lI1l1Il1l(Il11I1ll1III):
                    IIlIII1lIlll = l1I1lI1Illl1
                else:
                    IIlIII1lIlll = Il1l1lIIIIl1
                if IIlIII1lIlll == lII1IIII1I1I:
                    if not Il111II11lII(l1I1lI1Illl1):
                        IIlIII1lIlll = lII1lIlII111
                    else:
                        IIlIII1lIlll = l1I1lI1Illl1
                if IIlIII1lIlll == l1I1lI1Illl1:
                    I1I1IllIIIl1 = llI11IlllI1l
                if IIlIII1lIlll == ll11IIl11Ill:
                    I1I1IllIIIl1 = IIII1l1lIIlI
            if I1I1IllIIIl1 == IIl1Ill111Il:
                IlIll1Ill1I1_other_4854 = IlIll1Ill1I1_other_4854.__cast()
            if I1I1IllIIIl1 == Il11IIIlII1l:
                pass
            return not l11l11l11l1l(I111l111l1Il_self_30843.__cast(), IlIll1Ill1I1_other_4854)

        def __le__(self, other):
            (Ill1Il1llIIl_self_98421, Il1IIIII1I1I_other_22341) = (self, other)
            l1lIIII1l1I1 = lI11I11IIll1
            l1I1I1II1111 = II1l1llIlll1
            if not I1II1lI1IllI(Il1IIIII1I1I_other_22341, Promise):
                l1I1I1II1111 = lI11III11ll1
            else:
                l1I1I1II1111 = II11II11lI1l
            if l1I1I1II1111 == lI11III11ll1:
                if not llllIIIllIII(l1111ll1lI1I):
                    l1I1I1II1111 = lllI11I1I1II
                else:
                    l1I1I1II1111 = lIl111lIl1ll
            if l1I1I1II1111 == l1lIIll11lIl:
                l1lIIII1l1I1 = IIlI1l1lIIII
            if l1I1I1II1111 == lIIllI1IIl1l:
                l1lIIII1l1I1 = Il1IIl1l1lll
            if l1lIIII1l1I1 == lII1l1I1Il1l:
                II1IlIlIllII = I1I1Il1ll1ll
                if not l11lll1Il1II:
                    II1IlIlIllII = I111l1lIIl1I
                else:
                    II1IlIlIllII = IIl1Ill111Il
                if II1IlIlIllII == IIl1Ill111Il:
                    if not II111l1111ll.ll1lI1l1Il1l(lI1IIlII111I):
                        II1IlIlIllII = l1I1lI1Illl1
                    else:
                        II1IlIlIllII = I111l1lIIl1I
                if II1IlIlIllII == I111l1lIIl1I:
                    l1lIIII1l1I1 = l1l1lllIl1lI
                if II1IlIlIllII == lI1IIlII111I:
                    l1lIIII1l1I1 = I1ll1l1lIlIl
            if l1lIIII1l1I1 == l1IlI1llI1I1:
                Il1IIIII1I1I_other_22341 = Il1IIIII1I1I_other_22341.__cast()
            if l1lIIII1l1I1 == lll1ll1lllI1:
                pass
            return not I11I11l1lI1l(Ill1Il1llIIl_self_98421.__cast(), Il1IIIII1I1I_other_22341)

        def __gt__(self, other):
            (lIIIIlIIlIII_self_30911, l11I1ll1I1ll_other_51854) = (self, other)
            ll1IIII1l11I = l11llll1l1I1
            llIllll1ll11 = lI1llIllIlll
            if lII1IIll11l1(lI1Il1lIlIl1, lI1llIllIlll):
                llIllll1ll11 = l1llll1lllII
            else:
                llIllll1ll11 = Il1IIllI1III
            if llIllll1ll11 == lIllIIlIIIll:
                if not II1lII111Ill(l11I1ll1I1ll_other_51854, Promise):
                    llIllll1ll11 = IIl1Ill111Il
                else:
                    llIllll1ll11 = l1lIl1IIIllI
            if llIllll1ll11 == lIlIlI1I1I1I:
                ll1IIII1l11I = llllI1Ill111
            if llIllll1ll11 == llI11IlllI1l:
                ll1IIII1l11I = I1ll1l1lIlIl
            if ll1IIII1l11I == I1lIII1I1Il1:
                llllIIIl1IIl = lIIIl11III1I
                if not Il111II11lII(lll1ll1111ll):
                    llllIIIl1IIl = Il1lI11II1II
                else:
                    llllIIIl1IIl = l1lIIl1Il1ll
                if llllIIIl1IIl == l1lIIl1Il1ll:
                    if not Il111II11lII(Il111l111I11):
                        llllIIIl1IIl = Il1lI11II1II
                    else:
                        llllIIIl1IIl = IlI1lII1IllI
                if llllIIIl1IIl == Il1lI11II1II:
                    ll1IIII1l11I = lI11III1IIl1
                if llllIIIl1IIl == IlI1lII1IllI:
                    ll1IIII1l11I = Il11IIIlII1l
            if ll1IIII1l11I == lll1l11I11lI:
                pass
            if ll1IIII1l11I == Il1l1lIIIIl1:
                l11I1ll1I1ll_other_51854 = l11I1ll1I1ll_other_51854.__cast()
            return not IlIlIlI1lII1(lIIIIlIIlIII_self_30911.__cast(), l11I1ll1I1ll_other_51854)

        def __ge__(self, other):
            (II1I1I1III1l_other_87460, l1llIIII1l1l_self_58615) = (other, self)
            lIlll11llI1I = l1111llIIIll
            lI11Il1l11I1 = llIII1I11lll
            if not llllIIIllIII(lIIIl11III1I):
                lI11Il1l11I1 = I1lI1l1I111l
            else:
                lI11Il1l11I1 = I1ll1I1lI1l1
            if lI11Il1l11I1 == I1I11lI1lllI:
                if not llllIIIllIII(I1l1111111l1):
                    lI11Il1l11I1 = I1lIII1I1Il1
                else:
                    lI11Il1l11I1 = lll11IIII11I
            if lI11Il1l11I1 == I1lIII1I1Il1:
                lIlll11llI1I = llIII1I11lll
            if lI11Il1l11I1 == lll11IIII11I:
                lIlll11llI1I = l11II1I11I1l
            if lIlll11llI1I == l11II1I11I1l:
                Illl1Il1IlI1 = lIllIlI1111l
                if not I1II1lI1IllI(II1I1I1III1l_other_87460, Promise):
                    Illl1Il1IlI1 = l1l1lllIl1lI
                else:
                    Illl1Il1IlI1 = Ill1Il1l11lI
                if Illl1Il1IlI1 == IIlIIIlII1II:
                    if not II111l1111ll.ll1lI1l1Il1l(IIl11lllIIlI):
                        Illl1Il1IlI1 = Ill1Il1l11lI
                    else:
                        Illl1Il1IlI1 = lI1IIlII111I
                if Illl1Il1IlI1 == l1I1lI1Illl1:
                    lIlll11llI1I = I1lI1l1I111l
                if Illl1Il1IlI1 == l11I1ll1III1:
                    lIlll11llI1I = Il1l1lIIIIl1
            if lIlll11llI1I == lIIlI1lllII1:
                II1I1I1III1l_other_87460 = II1I1I1III1l_other_87460.__cast()
            if lIlll11llI1I == I1lIII1I1Il1:
                pass
            return not lI1lIIIllII1(l1llIIII1l1l_self_58615.__cast(), II1I1I1III1l_other_87460)

        def __hash__(self):
            lIII1lI1111l_self_40327 = self
            return l11IIlII1I11(lIII1lI1111l_self_40327.__cast())

        def __format__(self, format_spec):
            (lIlIl1I11I11_self_12295, I1IllII1llII_format_spec_99358) = (self, format_spec)
            return IlIl1IIllII1(lIlIl1I11I11_self_12295.__cast(), I1IllII1llII_format_spec_99358)

        def __add__(self, other):
            (l1l1l1IIlllI_other_13307, l1Il1llIlIIl_self_28504) = (other, self)
            return l1Il1llIlIIl_self_28504.__cast() + l1l1l1IIlllI_other_13307

        def __radd__(self, other):
            (Il1111ll1lll_self_60238, Ill11l1ll111_other_65678) = (self, other)
            return Ill11l1ll111_other_65678 + Il1111ll1lll_self_60238.__cast()

        def __mod__(self, other):
            (l111III11III_self_14399, l1lllI1l11Il_other_45924) = (self, other)
            return l111III11III_self_14399.__cast() % l1lllI1l11Il_other_45924

        def __mul__(self, other):
            (l1IIl1III1Il_other_35178, I1IlI11I11l1_self_16091) = (other, self)
            return I1IlI11I11l1_self_16091.__cast() * l1IIl1III1Il_other_35178
    for I1I11lII1111_resultclass_85184 in Il1II1ll1I1I_resultclasses_33174:
        IlIIllI1lIII = l1l1I1l11111
        I1II11I1lIl1 = l11lI1l1I1Il
        if not lllIII111ll1(I11lI11II1I1, I1Il1l1ll1lI):
            I1II11I1lIl1 = lIII1lII11lI
        else:
            I1II11I1lIl1 = l11II1I11I1l
        if I1II11I1lIl1 == IlI11lI11Ill:
            if not lllIII111ll1(I1lI111111lI, I1lI1l1I111l):
                I1II11I1lIl1 = ll11IIl11Ill
            else:
                I1II11I1lIl1 = IIIlI11llIIl
        if I1II11I1lIl1 == ll1lllIII1lI:
            IlIIllI1lIII = III1IlI1I1lI
        if I1II11I1lIl1 == I111lIll1lll:
            IlIIllI1lIII = ll1lIlll1IlI
        if IlIIllI1lIII == ll1lIlll1IlI:
            I1I1l1llII11 = I11I1lIl1llI
            l1lIl1l1IIII = IllII1lll1II
            I1l11Il1II11 = llI11IlllI1l
            lllI1llIIIll = I1Il1IIII1lI
            if not llllIIIllIII(I1ll1I1lI1l1):
                lllI1llIIIll = Il11IIIlII1l
            else:
                lllI1llIIIll = l1IllIlIIl1I
            if lllI1llIIIll == lllIl11lIlII:
                if not Il1lI11l1Il1:
                    lllI1llIIIll = lIIlI1lllII1
                else:
                    lllI1llIIIll = I11l1II1ll11
            if lllI1llIIIll == lII1IIII1I1I:
                I1l11Il1II11 = lll11IIII11I
            if lllI1llIIIll == ll11Ill1IlI1:
                I1l11Il1II11 = IllII1lll1II
            if I1l11Il1II11 == IllII1lll1II:
                I11llIl11Il1 = l1IllIlIIl1I
                if not lI1lIIIllII1(l11l1lI1ll1l, II1lI1Il1lII):
                    I11llIl11Il1 = II11lIIlll1l
                else:
                    I11llIl11Il1 = Il11I11l111l
                if I11llIl11Il1 == I1Il1IIII1lI:
                    if not IlIlIlI1lII1(lIII1II1IIlI, Il11IlllIl1I):
                        I11llIl11Il1 = l1lllI11I1Il
                    else:
                        I11llIl11Il1 = IIII1lI1l1l1
                if I11llIl11Il1 == I1II11lII11l:
                    I1l11Il1II11 = IllIl11IIIll
                if I11llIl11Il1 == Il11I11l111l:
                    I1l11Il1II11 = lIlllIIIlI1I
            if I1l11Il1II11 == lll11Il1lllI:
                l1lIl1l1IIII = Illll1111IIl
            if I1l11Il1II11 == II1lIII1IlI1:
                l1lIl1l1IIII = llIlI11111ll
            if l1lIl1l1IIII == IlI11l11III1:
                III1IlI11Ill = lIII11l11l1l
                IlIIlII11IIl = lIIl1I1I1IlI
                if not II111l1111ll.ll1lI1l1Il1l(lIllIlI1111l):
                    IlIIlII11IIl = III1II1I11II
                else:
                    IlIIlII11IIl = I1ll1I1lI1l1
                if IlIIlII11IIl == lI11lI11lll1:
                    if not llllIIIllIII(I11II11Il1II):
                        IlIIlII11IIl = I1ll1I1lI1l1
                    else:
                        IlIIlII11IIl = I1Il1IIII1lI
                if IlIIlII11IIl == I1Il1IIII1lI:
                    III1IlI11Ill = I1IIIlI1llll
                if IlIIlII11IIl == l11l1II1ll1l:
                    III1IlI11Ill = ll1lIlll1IlI
                if III1IlI11Ill == I1IIIlI1llll:
                    l1I1l11I11ll = I1I1I11lll11
                    if not Il11I11l111l:
                        l1I1l11I11ll = lI1lI1I11I11
                    else:
                        l1I1l11I11ll = ll111lIlll1l
                    if l1I1l11I11ll == lIII1II1IIlI:
                        if not II111l1111ll.ll1lI1l1Il1l(II1I1Ill11ll):
                            l1I1l11I11ll = IIIIl1Il1III
                        else:
                            l1I1l11I11ll = l111Il1IlIl1
                    if l1I1l11I11ll == l11lll1l11lI:
                        III1IlI11Ill = lIl1llIl11II
                    if l1I1l11I11ll == l1I11IlllIIl:
                        III1IlI11Ill = lI1llIllI1l1
                if III1IlI11Ill == I1lIII1I1Il1:
                    l1lIl1l1IIII = llIlll1l1I1l
                if III1IlI11Ill == lIl1llIl11II:
                    l1lIl1l1IIII = IlI11lI11Ill
            if l1lIl1l1IIII == I1l1ll111Il1:
                I1I1l1llII11 = I1l1111111l1
            if l1lIl1l1IIII == l1Il1ll11I1l:
                I1I1l1llII11 = l1IlI1llI1I1
            if I1I1l1llII11 == l1l1lllIl1lI:
                if not II111l1111ll.ll1lI1l1Il1l(lI11III11ll1):
                    I1I1l1llII11 = IIlIll1lI1Il
                else:
                    I1I1l1llII11 = IIllll1I11I1
            if I1I1l1llII11 == IIllll1I11I1:
                IlIIllI1lIII = l11lI1l1I1Il
            if I1I1l1llII11 == III1l11ll1II:
                IlIIllI1lIII = Il11I1ll1III
        if IlIIllI1lIII == llIlll1l1I1l:
            pass
        if IlIIllI1lIII == I11IIlIlllll:
            for I1Ill1lI11ll in ll11lIlI1I1I(IllIl11IIIll, IlIllllIIIIl):
                for l1l11I1ll1l1 in [lI1ll11lIlll]:
                    for ll1III1llIlI in l1Ill1lIl1I1(III111III1I1, l1IllIlIIl1I):
                        while ((not Il111II11lII(IlI11l11III1) or Il111II11lII(IlIIll1lIIll)) and (not Il111II11lII(l1lIIl1Il1ll) or llllIIIllIII(Il111l111I11))) and ((llll1lIlI1ll == II1IlI11Il1I or llllI1Ill111) and (Il111II11lII(l11llll1l1I1) and Il1I11III1ll)):
                            for II111I111II1_type__12527 in I1I11lII1111_resultclass_85184.mro():
                                Il111IIIl111 = l11l1II1ll1l
                                l1Il1I1lII1I = II11II11lI1l
                                if not llllIIIllIII(ll1IllII1llI):
                                    l1Il1I1lII1I = lIIll111lII1
                                else:
                                    l1Il1I1lII1I = II1lI1Il1lII
                                if l1Il1I1lII1I == ll1IllII1llI:
                                    if not Il111II11lII(I1lI1l1I111l):
                                        l1Il1I1lII1I = l11IlIll111I
                                    else:
                                        l1Il1I1lII1I = I11IlI11Ill1
                                if l1Il1I1lII1I == lIIll111lII1:
                                    Il111IIIl111 = l11llll1l1I1
                                if l1Il1I1lII1I == l11IlIll111I:
                                    Il111IIIl111 = II1I1Ill11ll
                                if Il111IIIl111 == l11llll1l1I1:
                                    l11lIl11ll1l = IlIII1111ll1
                                    if not llllIIIllIII(I1ll1I1lI1l1):
                                        l11lIl11ll1l = I111l1lllIl1
                                    else:
                                        l11lIl11ll1l = l1lll1lIl11I
                                    if l11lIl11ll1l == ll1ll1lI1IIl:
                                        I1llI1II = II1llI1II1II
                                        ll1lllI11l1I = lIIIl1lllI1l
                                        l1l1lIl1IIII = lIIlllIIIII1
                                        if lI1lIIIllII1(I1I1I111I11l, lI1I11lIIIII):
                                            l1l1lIl1IIII = Illll1111IIl
                                        else:
                                            l1l1lIl1IIII = lI1lIl1l1l1l
                                        if l1l1lIl1IIII == lllIllI1ll1I:
                                            if not II111l1111ll.ll1lI1l1Il1l(lII1II111lII):
                                                l1l1lIl1IIII = Il1lI11II1II
                                            else:
                                                l1l1lIl1IIII = I11l1lIIlI1I
                                        if l1l1lIl1IIII == lI1l1I111Il1:
                                            ll1lllI11l1I = IlI1lII1IllI
                                        if l1l1lIl1IIII == lI1I111lIIIl:
                                            ll1lllI11l1I = llIll1Il1II1
                                        if ll1lllI11l1I == l11llllIl1II:
                                            lI11IllIlIll = IlI11lI11Ill
                                            if not Il11I1ll1III:
                                                lI11IllIlIll = I1l1II1l1l1l
                                            else:
                                                lI11IllIlIll = IlIII1l11I1l
                                            if lI11IllIlIll == l11II1I11I1l:
                                                if not II111l1111ll.ll1lI1l1Il1l(IIlII11I11ll):
                                                    lI11IllIlIll = lIIl1I1I1IlI
                                                else:
                                                    lI11IllIlIll = lIlII1I111ll
                                            if lI11IllIlIll == lIIl1I1I1IlI:
                                                ll1lllI11l1I = l1llI1I1IlI1
                                            if lI11IllIlIll == lII1l1I1Il1l:
                                                ll1lllI11l1I = IIll1lllllIl
                                        if ll1lllI11l1I == llllI1Ill111:
                                            I1llI1II = III1II1I11II
                                        if ll1lllI11l1I == IIll1lllllIl:
                                            I1llI1II = lIIIlIIlI11l
                                        if I1llI1II == lll1II1I1I11:
                                            ll1lI1l1l111 = ll11IllI1lII
                                            IlIll1ll11Il = lI1lI1I11I11
                                            if not llllIIIllIII(II1IlI11Il1I):
                                                IlIll1ll11Il = l1llII1I1III
                                            else:
                                                IlIll1ll11Il = II1I1I11llll
                                            if IlIll1ll11Il == IIllll1llI11:
                                                if not lIlIlI1I1I1I:
                                                    IlIll1ll11Il = II1IlI11Il1I
                                                else:
                                                    IlIll1ll11Il = Il1IIII1lI1I
                                            if IlIll1ll11Il == lIlIll1lll11:
                                                ll1lI1l1l111 = l1llIIllIl11
                                            if IlIll1ll11Il == l1llIIllIl11:
                                                ll1lI1l1l111 = I1Il1IIII1lI
                                            if ll1lI1l1l111 == l11II1II11II:
                                                I1II1lllIl1l = ll11Ill1IlI1
                                                if not Il111II11lII(I11l1lIIlI1I):
                                                    I1II1lllIl1l = II11II11lI1l
                                                else:
                                                    I1II1lllIl1l = III11l11l1ll
                                                if I1II1lllIl1l == I1lIl1llIIll:
                                                    if l11l11l11l1l(IlIII11IlI1I, II111lI11l1l):
                                                        I1II1lllIl1l = IIllI111I1lI
                                                    else:
                                                        I1II1lllIl1l = Il1IIIIl1I11
                                                if I1II1lllIl1l == IIllIl1IllII:
                                                    ll1lI1l1l111 = I1l11IIIlIl1
                                                if I1II1lllIl1l == l1lIIll11lIl:
                                                    ll1lI1l1l111 = IlI11lI11Ill
                                            if ll1lI1l1l111 == l1llIIllIl11:
                                                I1llI1II = llIlIl1I1l1l
                                            if ll1lI1l1l111 == Il1lI11II1II:
                                                I1llI1II = lI11lI11lll1
                                        if I1llI1II == llIlIl1I1l1l:
                                            l11lIl11ll1l = l1llII1I1III
                                        if I1llI1II == III1II1I11II:
                                            l11lIl11ll1l = lI11I11IIll1
                                    if l11lIl11ll1l == l1llII1I1III:
                                        Il111IIIl111 = II1I1Ill11ll
                                    if l11lIl11ll1l == l1I1lI1Illl1:
                                        Il111IIIl111 = Illll11l11ll
                                if Il111IIIl111 == I111l1lIIl1I:
                                    pass
                                if Il111IIIl111 == II1I1Ill11ll:
                                    for l1l1l1lII1II_method_name_58458 in II111I111II1_type__12527.__dict__:
                                        lll1I11IlIlI = l11II1I11I1l
                                        llI11l11l1Il = I1IIIlI1llll
                                        llIl1IlII11I = IIlIll1lI1Il
                                        lII1I1l1lll1 = IlI11l1Il1II
                                        ll111111lIIl = IlIII11IlI1I
                                        if not Il111II11lII(IlI1lII1IllI):
                                            ll111111lIIl = I1I1I11lll11
                                        else:
                                            ll111111lIIl = Illll11l11ll
                                        if ll111111lIIl == lll1II1I1I11:
                                            if not I1II11lII11l:
                                                ll111111lIIl = II11lIIlll1l
                                            else:
                                                ll111111lIIl = llIlll1l1I1l
                                        if ll111111lIIl == lI11ll1Il1lI:
                                            lII1I1l1lll1 = IlIIl1l11l11
                                        if ll111111lIIl == I1I1I11lll11:
                                            lII1I1l1lll1 = I11l1lIIlI1I
                                        if lII1I1l1lll1 == I1llIIllII1I:
                                            llIl11llII1I = l11IlIll111I
                                            if not IllIl11IIIll:
                                                llIl11llII1I = IlIllllIIIIl
                                            else:
                                                llIl11llII1I = IIllll1llI11
                                            if llIl11llII1I == l11lllll1I11:
                                                if not II111l1111ll.ll1lI1l1Il1l(IlIIl1l11l11):
                                                    llIl11llII1I = IIllll1llI11
                                                else:
                                                    llIl11llII1I = Il11IlllIl1I
                                            if llIl11llII1I == IIllll1llI11:
                                                lII1I1l1lll1 = Il11l1l1l11l
                                            if llIl11llII1I == Il11IlllIl1I:
                                                lII1I1l1lll1 = Il1lIIll11l1
                                        if lII1I1l1lll1 == I11I1lIl1llI:
                                            llIl1IlII11I = lllIl11lIlII
                                        if lII1I1l1lll1 == Il1lIIll11l1:
                                            llIl1IlII11I = l1lIl1IIIllI
                                        if llIl1IlII11I == lllIl11lIlII:
                                            l1l1llIII111 = llll1l1IlI1I
                                            l11II1llI1l1 = Il1lI11II1II
                                            if lllIII111ll1(l11II1II11II, I1Il1IIII1lI):
                                                l11II1llI1l1 = l11lll1Il1II
                                            else:
                                                l11II1llI1l1 = lIIl1I1I1IlI
                                            if l11II1llI1l1 == l11lll1Il1II:
                                                if not llllIIIllIII(l1111llIIIll):
                                                    l11II1llI1l1 = I1l1II1l1l1l
                                                else:
                                                    l11II1llI1l1 = lI11I111lI1I
                                            if l11II1llI1l1 == lIIl1I1I1IlI:
                                                l1l1llIII111 = ll111lIlll1l
                                            if l11II1llI1l1 == l11II1I11I1l:
                                                l1l1llIII111 = IlI11l11III1
                                            if l1l1llIII111 == l11lllll1I11:
                                                lIl1lII1IllI = IlIII1111ll1
                                                if not II111l1111ll.ll1lI1l1Il1l(IlI11l11III1):
                                                    lIl1lII1IllI = lIl111lIl1ll
                                                else:
                                                    lIl1lII1IllI = lI1I111lIIIl
                                                if lIl1lII1IllI == IlI11lI11Ill:
                                                    if lI1lIIIllII1(II1IlI11Il1I, lIll111III11):
                                                        lIl1lII1IllI = ll11IllI1lII
                                                    else:
                                                        lIl1lII1IllI = l1lllIIIl11l
                                                if lIl1lII1IllI == ll11IllI1lII:
                                                    l1l1llIII111 = IlIIl1IIlIl1
                                                if lIl1lII1IllI == lII1Il1IlIl1:
                                                    l1l1llIII111 = I1lIl1llIIll
                                            if l1l1llIII111 == l1II1lll1I1I:
                                                llIl1IlII11I = III1II1I11II
                                            if l1l1llIII111 == II1I1lI111ll:
                                                llIl1IlII11I = III1IlI1I1lI
                                        if llIl1IlII11I == III1IlI1I1lI:
                                            llI11l11l1Il = l1llI1I1IlI1
                                        if llIl1IlII11I == III1II1I11II:
                                            llI11l11l1Il = Il11IIIlII1l
                                        if llI11l11l1Il == lI1llIllI1l1:
                                            if lI1lIIIllII1(I1I1lll1Il11, l1l11Il1lIll):
                                                llI11l11l1Il = IIlI1IIIl1II
                                            else:
                                                llI11l11l1Il = IIII1l1lIIlI
                                        if llI11l11l1Il == IlIllllIIIIl:
                                            lll1I11IlIlI = IlIllIIIIIIl
                                        if llI11l11l1Il == llIII1I11lll:
                                            lll1I11IlIlI = IlIIll1lIIll
                                        if lll1I11IlIlI == I1IlII1l111l:
                                            I11l1IIl11l1 = IlIIll1lIIll
                                            if not l1I11IlllIIl:
                                                I11l1IIl11l1 = lll11Il1lllI
                                            else:
                                                I11l1IIl11l1 = l1IllIlIIl1I
                                            if I11l1IIl11l1 == l1IllIlIIl1I:
                                                if l11l11l11l1l(lIIl1IlIlI1I, lI1llllI11I1):
                                                    I11l1IIl11l1 = lIl1l1I111lI
                                                else:
                                                    I11l1IIl11l1 = I1l1II1l1l1l
                                            if I11l1IIl11l1 == lll11Il1lllI:
                                                lll1I11IlIlI = lIlIll1lll11
                                            if I11l1IIl11l1 == llIlIll1l1ll:
                                                lll1I11IlIlI = lIl1llIl11II
                                        if lll1I11IlIlI == IlIIll1lIIll:
                                            IllIlIllIIIl = IlllI1I11I1l
                                            lI1I1I1I11II = lI1l1I111Il1
                                            if l11l11l11l1l(I1II111111Il, IlI11l1Il1II):
                                                lI1I1I1I11II = lllIl11lIlII
                                            else:
                                                lI1I1I1I11II = IIl11lllIIlI
                                            if lI1I1I1I11II == lIllIIlIIIll:
                                                if not lI11ll1111lI(__proxy__, l1l1l1lII1II_method_name_58458):
                                                    lI1I1I1I11II = ll111lIlll1l
                                                else:
                                                    lI1I1I1I11II = IIl11lllIIlI
                                            if lI1I1I1I11II == l1II1lll1I1I:
                                                IllIlIllIIIl = lIII11l11l1l
                                            if lI1I1I1I11II == lIIlllIIIII1:
                                                IllIlIllIIIl = l11llllIl1II
                                            if IllIlIllIIIl == IIl1IlllI1II:
                                                I11Illl1IIIl = IIIII1I11I1I
                                                if not llllIIIllIII(lII1lIlII111):
                                                    I11Illl1IIIl = IIII11I111l1
                                                else:
                                                    I11Illl1IIIl = l11II1I11I1l
                                                if I11Illl1IIIl == IlIII1l11I1l:
                                                    if l11l11l11l1l(l1lll1lIl11I, lIlIIlllII1I):
                                                        I11Illl1IIIl = l1lIIll11lIl
                                                    else:
                                                        I11Illl1IIIl = IlIIlll1llIl
                                                if I11Illl1IIIl == II11IlIIIl1I:
                                                    IllIlIllIIIl = I1l1II1l1l1l
                                                if I11Illl1IIIl == lllI11I1I1II:
                                                    IllIlIllIIIl = lI11I11IIll1
                                            if IllIlIllIIIl == lIIl1I1I1IlI:
                                                continue
                                            if IllIlIllIIIl == lIII11l11l1l:
                                                pass

                                            def __wrapper__(self, *args, __method_name=l1l1l1lII1II_method_name_58458, **kw):
                                                (lIIlllIII1l1_args_9116, llllI1IIll11___method_name_91213, IlIlIlll1IlI_kw_53203, llllll11IIIl_self_85109) = (args, __method_name, kw, self)
                                                I1IIIII1Il1l_result_48856 = lI1lIl1I11II_func_5233(*llllll11IIIl_self_85109._args, **llllll11IIIl_self_85109._kw)
                                                return IllIl111111I(I1IIIII1Il1l_result_48856, llllI1IIll11___method_name_91213)(*lIIlllIII1l1_args_9116, **IlIlIlll1IlI_kw_53203)
                                            IIlllII111Il(__proxy__, l1l1l1lII1II_method_name_58458, __wrapper__)
                                        if lll1I11IlIlI == Il111l111I11:
                                            pass
                            break

    @wraps(lI1lIl1I11II_func_5233)
    def __wrapper__(*args, **kw):
        (ll11Il1lllI1_kw_37181, l1lIlII1I1Il_args_95038) = (kw, args)
        return __proxy__(l1lIlII1I1Il_args_95038, ll11Il1lllI1_kw_37181)
    return __wrapper__

def lazy(func, *resultclasses):
    """
    Turn any callable into a lazy evaluated callable. result classes or types
    is required -- at least one is needed so that the automatic forcing of
    the lazy evaluation code is triggered. Results are not memoized; the
    function is evaluated on every access.
    """
    return ll1l1I11ll1l(func, *resultclasses)

def l1l1lIIlII1I(I1IIIIIIl11l_func_38196, IIll1111IlIl_kwargs_78982, ll111IlllI11_args_48009, *llI11lII111l_resultclasses_24661):
    return lazy(I1IIIIIIl11l_func_38196, *llI11lII111l_resultclasses_24661)(*ll111IlllI11_args_48009, **IIll1111IlIl_kwargs_78982)

def _lazy_proxy_unpickle(func, args, kwargs, *resultclasses):
    return l1l1lIIlII1I(func, kwargs, args, *resultclasses)

def l1l1IIIIIIII(lIl1I1lllllI_text_90003):
    """
    Shortcut for the common case of a lazy callable that returns str.
    """
    return lazy(I1lI11l11l11, I1lI11l11l11)(lIl1I1lllllI_text_90003)

def lazystr(text):
    """
    Shortcut for the common case of a lazy callable that returns str.
    """
    return l1l1IIIIIIII(text)

def I1l1lI11IIII():
    assert not lII1IIll11l1(lazystr(ll1l11l1lIlI), ll1l11l1lIlI)

def test_temp():
    return I1l1lI11IIII()

def Illl1lI11III(lI1IIIIl1llI_config_string_7828):
    IlIII1llII1I_color_settings_26501 = lll1ll1111ll
    for lIIlIlIlI11I_role_39717 in [Ill1l111Illl]:
        I1I11IIIIl1l = I11IlI11Ill1
        III1II111IIl = Il1lIIll11l1
        if not II111l1111ll.ll1lI1l1Il1l(llIlll1l1I1l):
            III1II111IIl = IIllIl1IllII
        else:
            III1II111IIl = Il11I11l111l
        if III1II111IIl == Il11l11IIIII:
            if lllIII111ll1(I1I1I11lll11, l1l11Il1lIll):
                III1II111IIl = lIl1I11l1l1l
            else:
                III1II111IIl = ll11I1111lIl
        if III1II111IIl == IIIlIl11lll1:
            I1I11IIIIl1l = l11l1II1ll1l
        if III1II111IIl == lIIllI1IIl1l:
            I1I11IIIIl1l = IIllI111I1lI
        if I1I11IIIIl1l == l11l1II1ll1l:
            lI1I1IlIl1I1 = II1IIIl111l1
            if not II111l1111ll.ll1lI1l1Il1l(l11IIIlIl11I):
                lI1I1IlIl1I1 = III1l1l111ll
            else:
                lI1I1IlIl1I1 = IIIIl1lIIl11
            if lI1I1IlIl1I1 == llll1l1IlI1I:
                IlIl1IIll1II = lIlIll1lll11
                l1lIl11l11II = Il11I11l111l
                I1111l11I111 = l1lIIll11lI1
                if not lI11ll1Il1lI:
                    I1111l11I111 = l11lll1l11lI
                else:
                    I1111l11I111 = II1IlII1II1I
                if I1111l11I111 == l11llllIl1II:
                    if not Il1IIIIl1I11:
                        I1111l11I111 = II1IlII1II1I
                    else:
                        I1111l11I111 = II1llIl1I1II
                if I1111l11I111 == ll11Ill1IlI1:
                    l1lIl11l11II = IIllIl1IllII
                if I1111l11I111 == II11lIlI111I:
                    l1lIl11l11II = II11IlIIIl1I
                if l1lIl11l11II == II11IlIIIl1I:
                    IlIIl11lIlII = llIIIlllI111
                    if l11l11l11l1l(lIIl1I1I1IlI, ll11Ill1IlI1):
                        IlIIl11lIlII = l11llll1l1I1
                    else:
                        IlIIl11lIlII = III111I11111
                    if IlIIl11lIlII == lIlII1I111ll:
                        if not lIl1lIlI1lI1:
                            IlIIl11lIlII = I11lI1lll1I1
                        else:
                            IlIIl11lIlII = lII1lIlII111
                    if IlIIl11lIlII == III111I11111:
                        l1lIl11l11II = IIllI111I1lI
                    if IlIIl11lIlII == lII1lIlII111:
                        l1lIl11l11II = Il1IIIIl1I11
                if l1lIl11l11II == IIllI111I1lI:
                    IlIl1IIll1II = l1Il1lII11Il
                if l1lIl11l11II == Il1IIIIl1I11:
                    IlIl1IIll1II = I1l1ll111Il1
                if IlIl1IIll1II == Il1lI11II1II:
                    Il1I11llII1I = II1IlI11Il1I
                    IIl1l1l1l1ll = I1IIIlI1llll
                    if lllIII111ll1(ll1I111Il1l1, lIIII1IIIIII):
                        IIl1l1l1l1ll = II1I1I11llll
                    else:
                        IIl1l1l1l1ll = I11lI1lll1I1
                    if IIl1l1l1l1ll == l1l1lI11I11l:
                        if IlIlIlI1lII1(IIl1IlllI1II, llI1l1IIIlll):
                            IIl1l1l1l1ll = II11lll1I1lI
                        else:
                            IIl1l1l1l1ll = lIllIlI1111l
                    if IIl1l1l1l1ll == IlIII1lI1lIl:
                        Il1I11llII1I = II1l1llIlll1
                    if IIl1l1l1l1ll == II11lll1I1lI:
                        Il1I11llII1I = I1llIIllII1I
                    if Il1I11llII1I == lII1II111lII:
                        Il1IIlll111l = I11I1lIl1llI
                        if not l11IlIll111I:
                            Il1IIlll111l = l11I1ll1III1
                        else:
                            Il1IIlll111l = ll11IIl11Ill
                        if Il1IIlll111l == ll11IIl11Ill:
                            if not II111l1111ll.ll1lI1l1Il1l(I11IIlIlllll):
                                Il1IIlll111l = l11I1ll1III1
                            else:
                                Il1IIlll111l = III1l11l11Il
                        if Il1IIlll111l == l11I1ll1III1:
                            Il1I11llII1I = lI1IlIlI1Ill
                        if Il1IIlll111l == l1l1I111l11l:
                            Il1I11llII1I = I11I1lIl1llI
                    if Il1I11llII1I == IllII1lll1II:
                        IlIl1IIll1II = l1Il1lII11Il
                    if Il1I11llII1I == Il11l1l1l11l:
                        IlIl1IIll1II = ll1lIlll1IlI
                if IlIl1IIll1II == ll1lIlll1IlI:
                    lI1I1IlIl1I1 = I1I11lI1lllI
                if IlIl1IIll1II == IlIIl1l11l11:
                    lI1I1IlIl1I1 = I1l11IIIlIl1
            if lI1I1IlIl1I1 == lI1llIllIlll:
                I1I11IIIIl1l = ll11IllI1lII
            if lI1I1IlIl1I1 == I1II11lII11l:
                I1I11IIIIl1l = IIllI111I1lI
        if I1I11IIIIl1l == ll11I1111lIl:
            pass
        if I1I11IIIIl1l == l1lIIll11lIl:
            Il11I1Il1Ill = ll1l11IIIIl1
            ll1IIllI1l1l = llII1lIll1ll
            if not IlIII1llII1I_color_settings_26501:
                ll1IIllI1l1l = lI1I111lIIIl
            else:
                ll1IIllI1l1l = II11lll1I1lI
            if ll1IIllI1l1l == lIllIIlIIIll:
                if not Il111II11lII(I1l1I111I111):
                    ll1IIllI1l1l = Illll1111IIl
                else:
                    ll1IIllI1l1l = II1l1llIlll1
            if ll1IIllI1l1l == lIII1lII11lI:
                Il11I1Il1Ill = lIII11l11l1l
            if ll1IIllI1l1l == IllII1lll1II:
                Il11I1Il1Ill = l1I1lI111Il1
            if Il11I1Il1Ill == Il1lI11l1Il1:
                l11lII1I111l = I1ll1I1lI1l1
                if not l11l1II1ll1l:
                    l11lII1I111l = ll1lII111IIl
                else:
                    l11lII1I111l = lll11IIII11I
                if l11lII1I111l == lll1I1lII1lI:
                    if not Il111II11lII(l1llII1I1III):
                        l11lII1I111l = llII1lIll1ll
                    else:
                        l11lII1I111l = lI11I111lI1I
                if l11lII1I111l == ll1lll1l1lII:
                    Il11I1Il1Ill = l1I1lI111Il1
                if l11lII1I111l == llII1lIll1ll:
                    Il11I1Il1Ill = l11l1II1ll1l
            if Il11I1Il1Ill == l1lIl1ll1I1I:

                def lIIl11lIll11_style_func_63097(x):
                    lII1IlIlllIl_x_46135 = x
                    return lII1IlIlllIl_x_46135
            if Il11I1Il1Ill == l1I1lI111Il1:
                lIIl11lIll11_style_func_63097 = I1I1Il1ll1ll
            IIlllII111Il(make_style, lIIlIlIlI11I_role_39717, lIIl11lIll11_style_func_63097)
    return Il11llIllll1

def make_style(config_string=''):
    return Illl1lI11III(config_string)