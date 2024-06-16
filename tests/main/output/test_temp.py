from functools import wraps
import codecs
(IIIlIl11II1I, IlIIIlIlIllI, l11Illl1IllI, I1IIl1lIl111, I1lI1lI1IIII, ll11IllI11II, ll1Il11ll11l, llII1IIlI11I, ll1l1lIll1l1, lIlII1l1lIl1, ll1llll1lI1l, Il111ll11lII, l1IIIl1lII11, IIl111ll1I1I, I11l111I11I1, IlllllII1lIl, lII1lllll1II, IlIIII111l1I, IIlII1lI111I, lII1Ill1II1l, ll1ll1II1l1, lIIllIl1ll1I, I1IlIIl1llIl, lllllIlIII1I, lI11lIlll1I1, lI11llIl1l1l, lI111III1II1, llIIIIlIlIIl, lIll11IlII1I, lIIIlI11lIl1, lIIlIl11Illl, lI1lII11llll, II11II11I11I, l1Ill111l111, ll1I1II111II, I111111I1IIl, IIIll1lI11ll, l11lI1111llI, llI1llIIlllI, l1lIlI1Ill11, I1lI1lI1ll11, l11lII11llll, llllI11IIIII, IIII1IllIIlI, lI1ll11I11Il, IIl111I11l11, I1III1IIl1Il, lII11IlIIl11, llI1IIllI1lI, IIIII1llIl1l, l1Illl111l1l, IIIlII11ll1I, l1IlllIIIlII, IIlIIllll11l, IlllllI1I1lI, l111I1I1I1lI, IIIllI1l1I1I, lI11III1ll1l, lII1II1l111I, l1l1ll1ll1I1, I1lll111IIll, ll1ll1Il11Il, lIIIIllIII1I, Illl1ll1l1lI, lIIIlIl11II1, l1IIIlIll1l1, lIIl1II11lII, lIl1IlII11Il, III11lIlllII, lII11lIIIIlI, l1l1I1IIl1l1, I1IlIIIlllII, l1ll1IIlIlII, I111l11lIlIl, I1lII1Il1lI1, I1lllIIl11Il, IIll1Il1Il1I, l11111IlIIl1, Il1l1I11lIIl, IllI1I1lI1l1, lI1lIl1llIIl, IlI1lI1lI1Il, lIIIIlII1lll, IIIIIll1llII, IlIl1I111I11, I1lI1lllIIll, lIIIIIIl1IIl, I1I1l111ll1I, III1II1II1II, lIIll11I1IIl, IlII111III1I, ll1l11Il11Il, llIlI11Ill1I, ll1lllIlll1l, IlIlll11I1lI, l1I11llIl1II, l1I1I11IlllI, lIl1I111l111, Ill1I11Ill11, IllI1lI1lI1I, l11lll1lllII, ll1lll1l1II1, lIll1lIlIIIl, lI1IIIllll11, IIII1IIIlI1I, Il111I1I1I1l, l1Il1IIIII1l, lI111Il1lII1, Il1IlI1111ll, l1llIIlI1l1I, IIl1IIllI111, I11IIIlI1I11, l1II1I1Il1ll, I1lllIIII1I1, ll1111II1I11, IllI1111I1I1, II1IIlIl1lIl, Il1II1I1I11l, I1lI1l111lII, lI11l1llI111, IIIlll1ll111, IIIll1lllIII, III111Illl1l, IIl11I1IllII, lIII11lIIl1l, IlllIIl1111I, II1lIllIll1l, Il1l1I1III1I, I1lI1llIll11, IlIllllI11Il, II1l1I1IIIl1, I11l111IlIIl, IIlIIIllll1l, II1lll1l11I1, l1Il1lI1l1ll, l11IIIllIl1l, IlII1lI1Il11, llIlI1I1111l, IlllI1I11I1I, I1II1I1II1I1, I1IIl111III1, lIl1lIllI1l1, I1II1IIlI1Il, II1IIl1lIIIl, ll1Ill1l1II1lIII11, ll1llll111Il, ll1IlllII11I, Il111lI1Il1l, l1llllIl1Il1, lIIlll1l1l1l, llII1lIllIll, l111IIllII11, IIl11l1111ll, l11l1II11l1l, l11IIl1IIllI, I11Il1llI11I, ll1I1IIllII1, IlIIl1IlIlII, l11lIl1IIl1I, l11Il11lIIlI, IIIIIIIllIll, l11lI1lllll1, llII111lIIlI, lIl1I1llll1I, llIll1l11III, Il11Il11lllI, lI11Il111III, l1Il1I111l1l, lII1l11II1lI, lIlIllI111lI, l1lIIl1Il1Il, ll1Il1I1Il1I, ll1I1l1I1111, Ill111l1lII1, llI11IIl1l1l, Ill11llll11I, Il111lIII1Il, ll1lI1I1Il1l, lIl1l111I11l, IIl1llI1I1l1, II1l1ll11l1l, l11111l111lI, l11l11l11Ill, ll111lllI11l, I1II11llI111, II111I11IIl1, lI1111lI11l1, l1Il1111I1l1, IIIllIlIIII1, I11IlI1111I1, I11IIl1l11l1, I1lIl1l1l11I, I11lI1lIII1l, lII1111l111l, lI1lI111IIIl, lllllIIlIII1, l1llIIll1III, lI1lll1lI1Il, llllII1llI1I, l1I1ll1lII1l, lllIll1l111l, lI1IIIl11lll, IlIIlIIlI1l1, II1I11l11lI1, l11ll11lIlII, lllI11lIl1I1, IIlI1l1IlIl1, I1IIIII1I1Il, I1l1IllIII11, I11lIll11lII, lIIl1II11I1l, IIllI1llIlIl, I1Ill1lIIlIl, Il11II1I1ll1, I1I1IllI1Il1, llIII1II1lII, Il111l11l1ll, Il11I1I1II1l, lIlII1IlI1Il, Il11llI1llII, IlI1Il1IlIll, IIIl1l1II111, I11Illl1lIII, lllIl11I1l1l, Ill111l1ll11, l1IIlIllI11I, I11IIl1IIIII, ll1I11Il1lI1, l11lIIIllI11, llllI1I11lIl, II11Il1111ll, IIIII11lI1Il, ll111Ill1Il1, l1I11llI11Il, I1Il11Ill1Il, lllI11lIIIl1, lI1l11lI1l11, I1ll1lIlIllI, ll1I1lIIIlII, l1l1l11IlI11, l1lIIIl1IlIl, I1IIII11I1Il, I1l1lllIlII1, I1I11ll1I11I, l1I1ll111III, II1l11llI111, IIIIIIl11IIl, lIll1Il1lI11, llI1IlIIl11I, lI1lIl1I1IIl, IIl1ll1lll11, l1I111ll1llI, ll1IIlII1l1I, Il11l1lIII11, llIlIl1lIlIl, lll11IIl1I1l, I1111I1IIll1, IllIll1IlIll, Ill1lll1I1l1, l1l11IlII111, I1IlI1Il11ll, lI1l1III111I, I11I1lIllIl1, Il1I1111ll11, llIlIl1IllII, lI1II1l111I1, l1IlllII1I1I, lI1llllIll1I, I11ll11lll1l, II1lI11IllIl, lIl11l1ll1II, Il11llI1Il1l, IIlII1l1lII1, l1Il1111l1II, I1lll1l11l1l, I1l11ll1IIll) = (731149084 ^ 875506716 ^ 277589282 + 254783970, 360900878 - -574882917 ^ (966968055 ^ 241446818), 117290816 ^ 192932987 ^ ~-226646889, ~-973357973 ^ (370633162 ^ 739453528), ~(598117097 - 598117165), 683570038 ^ 108489419 ^ (336461904 ^ 986126818), 453663071 ^ 374373934 ^ (397033584 ^ 451962665), 541163138 + 347054884 - (562573435 ^ 360255973), 554501041 ^ 391334132 ^ (417929852 ^ 783765798), (79692683 ^ 280324927) - (518160503 ^ 177727702), ~(291042911 - 291042960), ~-198998401 ^ (758737568 ^ 652546873), ~-(53447676 ^ 53447630), ~-(344185471 ^ 344185456), 684927308 ^ 719546497 ^ (622210550 ^ 656829485), 180143876 - -33447069 ^ 664553304 - 450962329, 645841646 - -190509082 ^ 211651325 + 624699425, 233028930 + 508938812 + (823799461 + -1565767154), ~-~-13, ~-100978734 - ~-100978710, ~-205096386 + -~-205096368, (129338904 ^ 180856802) + (882337710 + -1107923330), ~-850079339 ^ (217008397 ^ 1044670327), (852001558 ^ 443011182) + -(931125515 ^ 533760635), 259964994 - 25882637 ^ 961372861 - 727290527, 532366772 + 415914265 + (682311206 - 1630592217), (214627438 ^ 327957591) + (495357120 + -1020089571), 483100113 ^ 243038273 ^ (354519753 ^ 127301495), ~-(220206410 ^ 220206440), str, 86336728 - -428432639 ^ ~-514769371, ~-(327598475 ^ 327598523), 990391199 ^ 1004821555 ^ (368502061 ^ 354062978), (491882168 ^ 492834155) + -~-3247059, ~(960961231 + -960961250), 376918535 ^ 362298180 ^ (621876366 ^ 654212570), 807071226 + -500221168 - (539470557 ^ 846037563), 521418114 ^ 763311662 ^ (846517022 ^ 2085023), 157705782 ^ 650898968 ^ (841873306 ^ 494960534), ~-248785356 - (119517323 + 129267990), ~(330736485 + -330736497), 366298406 ^ 588126384 ^ ~-920346063, 154686277 ^ 661782997 ^ ~-776622726, (119998700 ^ 770186978) - ~-718214619, ~-309784496 + (357242784 - 667027250), 193195235 - -280346116 ^ (230496296 ^ 293909189), 339758407 ^ 806260659 ^ (747412906 ^ 146956110), 840981527 - 835607473 + (313777744 - 319151751), 605427619 ^ 575875671 ^ (160357027 ^ 265021250), 761776621 - -52135661 ^ (922090571 ^ 108440736), 197830288 ^ 610944176 ^ ~-799072818, 656852022 ^ 343510636 ^ 995007900 + -133124953, 641422566 + -369526365 ^ (769140350 ^ 1038936288), 908209677 + -304374883 - (617688418 - 13853661), ~-586401767 - (791723191 ^ 230914829), 539367958 ^ 164673087 ^ (456671334 ^ 852421726), 177584969 - -558720090 + -(467087841 ^ 808726165), 672607622 ^ 974940838 ^ (347568976 ^ 112999518), 20671912 ^ 739806106 ^ (743547801 ^ 24266231), ~-15326446 ^ (702318435 ^ 691362735), ~(601521172 + -601521206), 317295892 ^ 596939394 ^ ~-830283676, isinstance, 275761055 ^ 350294226 ^ ~-76470142, ~-933680420 ^ (193820386 ^ 1009492896), 658818706 + 87998258 ^ (602048776 ^ 258018501), 320173109 ^ 731672475 ^ 302211151 - -646298470, 904714721 + -127524186 + -(96986083 ^ 731193185), 874814489 + -200120807 - ~-674693643, 575484765 - -51435453 ^ 387869956 + 239050265, 565579372 + 402110377 ^ ~-967689782, (492340650 ^ 481031911) - (435610956 ^ 403019368), 753472060 ^ 382385385 ^ (742595081 ^ 375436529), ~-(187558665 ^ 187558720), ~-~-46, 295859437 ^ 483368243 ^ ~-225307102, ~-346591184 + -(185092152 ^ 530630547), 176809410 - -555454522 + (894163737 + -1626427658), 755283130 ^ 848434177 ^ 280302742 + 249662474, ~-423985897 + -(212901770 ^ 368385366), ~-313900922 ^ (459380098 ^ 164899538), 862695610 - 35928016 ^ (423848396 ^ 671355196), 127516460 + 568486052 ^ 535965013 - -160037515, 194982392 + -95919467 - (748502893 ^ 695905031), (471512637 ^ 767450067) - (617397822 ^ 359158771), ~(633231659 - 633231710), 787236826 ^ 51238011 ^ (926423688 ^ 450464054), 78517879 + 506139446 - (504062714 ^ 1020414844), 164154095 + 670252420 + -~-834406484, 21417974 ^ 70246754 ^ (538367015 ^ 629144204), 676700112 ^ 267218574 ^ (139657789 ^ 803992389), ~-~-6, 55121957 ^ 968148596 ^ 544720148 + 444995896, 615367281 - 221320906 + -(193196300 ^ 486496889), (983707801 ^ 11713156) - (365348360 ^ 802573339), 676163398 + -447469255 ^ ~-228694143, ~-363189471 + (533024010 - 896213448), ~-294130704 ^ (803759768 ^ 1046508222), ~(977892919 + -977892929), ~(190010467 + -190010475), 744932195 ^ 966148433 ^ 442150320 + -74066811, repr, 99668429 - -790350761 + -(345718776 ^ 563585674), 'aaa'[::-1], 454657977 ^ 428935766 ^ 651397847 + -608894210, ''.join([chr(lI1I1lI11111 ^ 35077) for lI1I1lI11111 in [35172, 35172, 35172]]), 393553628 + -217183547 ^ (973240336 ^ 813779378), (799220424 ^ 132793368) + (715528936 + -1391428019), 414142318 ^ 902599805 ^ (487103611 ^ 812336931), 249933503 ^ 565126938 ^ (65528639 ^ 749562510), 237137522 - -530868699 ^ (672833003 ^ 98321831), (616517176 ^ 712607332) + (968489992 - 1216398396), 900037106 ^ 813169173 ^ (211474470 ^ 155737059), (559054287 ^ 995650164) - (221268738 - -215600277), ~-348545831 + (298002862 + -646548658), (2806082 ^ 901654622) + -(647662695 ^ 319714670), 101207695 ^ 592822161 ^ (799037885 ^ 184395965), 316902102 - -30611008 ^ 288178445 + 59334645, 52099620 - -522178260 + -(529335057 ^ 1035455434), id, (178499710 ^ 268719971) - (930291034 ^ 768932776), 992482265 ^ 38332907 ^ 534867910 + 427788912, 317093422 + 194194743 ^ (667001410 ^ 968360248), (723766183 ^ 822533106) + -(229449697 ^ 394792885), 560927435 - 88895912 ^ ~-472031506, 379762338 + 1042965 + -(381014212 ^ 487532), 249877400 - 243383964 ^ (641037474 ^ 643194949), 836773426 + -130575592 ^ ~-706197853, ~-(906994886 ^ 906994911), 993192975 - 382244727 ^ ~-610948288, 592454433 ^ 317271537 ^ (925313918 ^ 111027624), ~-(725262536 ^ 725262569), 305483802 + -60632943 ^ (621622422 ^ 731190322), 839773428 + -741782178 ^ 943244513 - 845253261, 326504838 + 557647169 ^ 12886422 - -871265584, 536037018 - -47585310 - (344897394 ^ 910682622), 185841515 + 561645324 - (344454547 ^ 940198799), 467714112 ^ 236076004 ^ 70188403 - -298057263, (317081055 ^ 575542021) - (931195359 ^ 120110858), 819430007 + -439371803 ^ 394369587 + -14311365, ~-719330547 ^ (945323668 ^ 314073674), ~-750208871 - ~-750208846, codecs.decode('nop', 'rot13'), ~-935456549 ^ (8784015 ^ 927459244), isinstance, ~-131547757 + -(127775193 ^ 4912049), ~(622496688 + -622496710), 610804543 - -50266938 ^ 259929538 - -401141946, hasattr, 115847915 ^ 123865934 ^ (441222748 ^ 466173911), 422912667 ^ 461105499 ^ (546368667 ^ 584984378), ~-846635404 + -(710305069 ^ 404800683), ~-(635248367 ^ 635248323), 650036047 + -588737051 ^ (569174543 ^ 575386408), ~-~-22, ~-733594496 ^ (453305686 ^ 817702411), ~-765267846 - ~-765267827, 923143740 - 73387174 ^ (944195896 ^ 182520034), ~-34059214 ^ (447246914 ^ 414171554), (149761739 ^ 1066905940) - (77530425 + 853252693), setattr, 230292851 - -95172863 + -(442085882 ^ 155158463), 942378028 ^ 804044706 ^ 305138345 + 93792503, 339204519 ^ 1060900776 ^ (691064606 ^ 37427470), ~(211344069 - 211344095), 10348523 ^ 35437603 ^ 779709381 - 737677278, 674304004 + 216995812 ^ (122347162 ^ 845871461), 886909339 ^ 1059595461 ^ (751478325 ^ 658484047), 483516782 ^ 359347954 ^ (730817810 ^ 573944490), range, isinstance, 633863523 - -49196296 ^ (799708164 ^ 119291487), str, (678196334 ^ 276137507) + -(307131649 ^ 710379334), ~-203875165 + (913837667 + -1117712768), 388889936 ^ 940596162 ^ (848645236 ^ 497609450), (399851145 ^ 810714880) + (118719889 - 781926096), ~-16037857 ^ (465386143 ^ 457805121), ~-~-17, 828141935 - 15920211 ^ ~-812221732, 491330853 + 226994070 ^ 345862877 - -372462011, format, ~-573995934 - ~-573995899, 588645102 - 313301623 - (782322948 - 506979480), 319848424 + 572247197 ^ 734328504 + 157767144, 301393976 ^ 327752504 ^ ~-41939771, 456286483 - 218362092 ^ 37710427 - -200213970, ~-(463479719 ^ 463479716), 746727773 + -667351363 + (229937321 + -309313703), 836074360 - 164126239 ^ (949367983 ^ 278604276), 622314859 ^ 758045544 ^ ~-137960996, ~-(394312573 ^ 394312567), 805877285 - 605435265 ^ ~-200442045, ~-555238126 ^ (591002740 ^ 35765947), 868143092 - 583863512 ^ (971267927 ^ 689282117), 931621964 + -352476759 - (521266415 + 57878743), ~-763906737 ^ 545511916 - -218394813, 35960526 + 717603958 - (747110241 ^ 7177289), isinstance, (786831643 ^ 130888105) - (226077960 ^ 609387904), ~-698024043 - (609607466 + 88416569), ~-163282230 - (259782717 + -96500511), ~-405366762 - (981474801 ^ 581532235), 643511822 + 56956188 - ~-700467981, ~-888539206 ^ (316910697 ^ 638952575), 811492379 ^ 341192127 ^ (714670265 ^ 244402438), ~-66092701 ^ ~-66092687, 402854663 + 73721449 ^ (692597381 ^ 892324841), 502459211 ^ 727032477 ^ 622098787 - -294834273, 980311907 ^ 518383299 ^ ~-613136769, ~-765557871 + (417465875 + -1183023708), getattr, None, 356253526 ^ 1027110029 ^ (666938687 ^ 264447692), 465858170 - -530708863 ^ (828717975 ^ 167992394), 355975440 + -16959029 - (866188527 ^ 664012349), 156312874 ^ 424913402 ^ (29806169 ^ 298074760), (849677819 ^ 989928201) + -(564823537 ^ 672043828), 490941560 - -144588407 ^ 571430725 - -64099232, 305048575 ^ 135329870 ^ (49704508 ^ 415776153), codecs.decode('nop', 'rot13'), 84270426 ^ 464468067 ^ ~-514516283, (340875086 ^ 50019031) - ~-380267888, 994341546 - 612651589 - (379963100 ^ 6678153), setattr, 268366169 - 234009951 ^ 218703713 + -184347513, 663518246 - -192079504 ^ (454422357 ^ 703237623), 256724649 + -217992271 ^ (125910835 ^ 97402226), ~-891026665 + (940026856 + -1831053512), 461912047 - -517034418 ^ ~-978946473, ~-~-15, ~-538941317 ^ (428022811 ^ 966560719), 559179022 ^ 719172293 ^ ~-193583056, ~(478707812 + -478707819), 888224982 - 111113557 - (828384349 ^ 523363073), (151269618 ^ 376882283) + -~-527627387, (449421891 ^ 296568147) + (231935213 + -423097327), 208689204 + -89547969 ^ (424225484 ^ 508615048), ~-72923683 ^ (859547745 ^ 929239633), 611416860 + 30987076 ^ 932630422 - 290226502, ~-570757118 ^ (834963532 ^ 331450281), hash, (688409038 ^ 540771332) - ~-154389915, ~-16740021 ^ 249926166 + -233186135, 471683891 ^ 1029799858 ^ 226366522 - -335419490, 57978901 ^ 755056773 ^ ~-779481276, 239712738 + -151548707 ^ ~-88164001, ~-(70319358 ^ 70319316), 842642187 + -213022507 ^ (103540368 ^ 598531415), 974609112 ^ 461901353 ^ 97272943 + 466817163, 98758656 - -743342378 + -(586518033 ^ 281345773), (590104012 ^ 443143581) + -(646385540 ^ 532848579), (909940223 ^ 285238143) + (24171812 + -682478488), 245396766 ^ 799923285 ^ 205837246 - -348706199, 631361237 - 37112178 + -(382978933 ^ 901271115), 883687960 + -744335398 ^ ~-139352561, ~-618349510 ^ (609942627 ^ 8503172), ~-629689580 ^ 447551471 + 182138091, (767885179 ^ 787306598) + (173165391 + -226226752), 876935339 - 244882863 ^ 319787103 + 312265281, ~(189366030 + -189366036), ~-561752013 ^ (521685201 ^ 1046736647), ~(179456891 + -179456914), 842169563 - 540135804 ^ (104860528 ^ 339779616), 396069464 ^ 3580324 ^ 391410397 + 5814542, 806962831 ^ 899233270 ^ (283964124 ^ 359432638), ~-381578588 - (369362932 ^ 12217014), ~(328275746 - 328275756), (145407706 ^ 304832980) + (112791970 + -557510824), (524791989 ^ 739349156) - (954875203 ^ 196877445), ~-(21873835 ^ 21873840), 309149055 + 589389338 ^ (683340568 ^ 489973910), 12557954 ^ 825554072 ^ ~-831220237, 918376892 ^ 76153599 ^ ~-842486636, (685007631 ^ 1057587373) - (819294039 - 418876356), 526921003 - -36125227 ^ (352869922 ^ 881277249))

def lIl1Il11I11I(l1II1II1llIl):
    return True

def lII1IlIll1Il(l1II1II1llIl):
    return l1II1II1llIl

class Il1II1l1Ill1:

    @staticmethod
    def lII1I1II1I1l(l1l1I1I11ll1):
        return True

    @staticmethod
    def IIIl1I1111lI(l1l1I1I11ll1):
        return l1l1I1I11ll1
l1ll1IllIlll = lambda Ill1IlII1111: True
I11I11Il11Il = lambda Ill1IlII1111: Ill1IlII1111

def ll1ll11l1IIl(lI1llll111l1, lIlIIIlIlll1):
    try:
        return lI1llll111l1 != lIlIIIlIlll1
    except:
        return not lI1llll111l1 == lIlIIIlIlll1

def Ill1lIll11II(l1I1IlIlIII1, II1I11lI1IIl):
    try:
        return l1I1IlIlIII1 == II1I11lI1IIl
    except:
        return not l1I1IlIlIII1 != II1I11lI1IIl

def l1llII1lII1I(llIl11llIl1I, I1II1l1lIlIl):
    try:
        return llIl11llIl1I >= I1II1l1lIlIl
    except:
        return not llIl11llIl1I < I1II1l1lIlIl

def l1I111lll1II(lIl1111Il1lI, I11II1I1I1l1):
    try:
        return lIl1111Il1lI > I11II1I1I1l1
    except:
        return not lIl1111Il1lI <= I11II1I1I1l1

def Il111IllIlII(Il11I111I1ll, llIllI11l11l):
    try:
        return Il11I111I1ll <= llIllI11l11l
    except:
        return not Il11I111I1ll > llIllI11l11l

def Illlll111lIl(ll1l1IlllII1, lllIlllllI1l):
    try:
        return ll1l1IlllII1 < lllIlllllI1l
    except:
        return not ll1l1IlllII1 >= lllIlllllI1l

class Promise:
    pass

def IlIl1I111lI1(IlIIlIlIIlII_func_65662, *lI11llI1Il1l_resultclasses_59483):

    class __proxy__(Promise):

        def __init__(self, args, kw):
            (I1l1lI1l1ll1_self_45661, l1Il1Illl11l_args_25944, ll1I11I1IllI_kw_85969) = (self, args, kw)
            I1l1lI1l1ll1_self_45661._args = l1Il1Illl11l_args_25944
            I1l1lI1l1ll1_self_45661._kw = ll1I11I1IllI_kw_85969

        def __reduce__(self):
            IllIl1llII11_self_48218 = self
            return (_lazy_proxy_unpickle, (IlIIlIlIIlII_func_65662, IllIl1llII11_self_48218._args, IllIl1llII11_self_48218._kw) + lI11llI1Il1l_resultclasses_59483)

        def __deepcopy__(self, memo):
            (IlllI1IIIIll_self_99159, l1I1lII1Il1I_memo_47389) = (self, memo)
            l1I1lII1Il1I_memo_47389[lI11l1llI111(IlllI1IIIIll_self_99159)] = IlllI1IIIIll_self_99159
            return IlllI1IIIIll_self_99159

        def __cast(self):
            III1lIlIlIl1_self_93884 = self
            return IlIIlIlIIlII_func_65662(*III1lIlIlIl1_self_93884._args, **III1lIlIlIl1_self_93884._kw)

        def __repr__(self):
            II1II1I1lI1l_self_80924 = self
            return ll1lll1l1II1(II1II1I1lI1l_self_80924.__cast())

        def __str__(self):
            llllII1l1111_self_84920 = self
            return ll1I1l1I1111(llllII1l1111_self_84920.__cast())

        def __eq__(self, other):
            (IlIlII1IllI1_other_1061, I1llII1II1lI_self_65183) = (other, self)
            IllI11Il1lIl = lIIl1II11lII
            lIl1I1IIIIII = l1I111ll1llI
            if not l1I11llIl1II:
                lIl1I1IIIIII = I11lIll11lII
            else:
                lIl1I1IIIIII = lII1Ill1II1l
            if lIl1I1IIIIII == I11lI1lIII1l:
                if not lIIIIllIII1I(IlIlII1IllI1_other_1061, Promise):
                    lIl1I1IIIIII = l11lIIIllI11
                else:
                    lIl1I1IIIIII = l1l1I1IIl1l1
            if lIl1I1IIIIII == I11lIll11lII:
                IllI11Il1lIl = IllI1I1lI1l1
            if lIl1I1IIIIII == I11ll11lll1l:
                IllI11Il1lIl = II11II11I11I
            if IllI11Il1lIl == IllI1I1lI1l1:
                l111lI1Ill11 = ll1IlllII11I
                if not lIl1Il11I11I(I1l1lllIlII1):
                    l111lI1Ill11 = I1lI1llIll11
                else:
                    l111lI1Ill11 = Ill11llll11I
                if l111lI1Ill11 == Ill11llll11I:
                    if not lIl1Il11I11I(ll1111II1I11):
                        l111lI1Ill11 = l1lIIIl1IlIl
                    else:
                        l111lI1Ill11 = II11II11I11I
                if l111lI1Ill11 == I1lI1llIll11:
                    IllI11Il1lIl = II11II11I11I
                if l111lI1Ill11 == IIIl1l1II111:
                    IllI11Il1lIl = IIl11l1111ll
            if IllI11Il1lIl == IIIl1l1II111:
                pass
            if IllI11Il1lIl == II1l11llI111:
                IlIlII1IllI1_other_1061 = IlIlII1IllI1_other_1061.__cast()
            return not ll1ll11l1IIl(I1llII1II1lI_self_65183.__cast(), IlIlII1IllI1_other_1061)

        def __ne__(self, other):
            (I1ll11I111lI_other_94146, lII1llllII11_self_74562) = (other, self)
            lIIIl11III1l = llII1lIllIll
            I1l1lI1111I1 = l1Ill111l111
            if not lIl1Il11I11I(ll1Il1I1Il1I):
                I1l1lI1111I1 = llIlI11Ill1I
            else:
                I1l1lI1111I1 = II1lll1l11I1
            if I1l1lI1111I1 == II1lll1l11I1:
                if not lllI11lIIIl1:
                    I1l1lI1111I1 = I1lI1l111lII
                else:
                    I1l1lI1111I1 = Il1I1111ll11
            if I1l1lI1111I1 == llIlI11Ill1I:
                lIIIl11III1l = I11I1lIllIl1
            if I1l1lI1111I1 == IlllIIl1111I:
                lIIIl11III1l = IIIllI1l1I1I
            if lIIIl11III1l == IIIllI1l1I1I:
                IlIIIllII1ll = IIIlIl11II1I
                if not l1ll1IllIlll(l11lIIIllI11):
                    IlIIIllII1ll = IIlII1lI111I
                else:
                    IlIIIllII1ll = lI11llIl1l1l
                if IlIIIllII1ll == lI11llIl1l1l:
                    if not l1lIIl1Il1Il(I1ll11I111lI_other_94146, Promise):
                        IlIIIllII1ll = IIlII1lI111I
                    else:
                        IlIIIllII1ll = I1IlIIIlllII
                if IlIIIllII1ll == lI1lIl1llIIl:
                    lIIIl11III1l = Il1l1I1III1I
                if IlIIIllII1ll == IIlII1lI111I:
                    lIIIl11III1l = l1I111ll1llI
            if lIIIl11III1l == lII1lllll1II:
                I1ll11I111lI_other_94146 = I1ll11I111lI_other_94146.__cast()
            if lIIIl11III1l == IIl111I11l11:
                pass
            return not Ill1lIll11II(lII1llllII11_self_74562.__cast(), I1ll11I111lI_other_94146)

        def __lt__(self, other):
            (llI1IlIllll1_self_92158, l11lll11I11l_other_47990) = (self, other)
            IIIIll1Illll = IlllllI1I1lI
            IlI1l1IIlllI = lI11Il111III
            if not l1ll1IllIlll(lllI11lIIIl1):
                IlI1l1IIlllI = IIIll1lllIII
            else:
                IlI1l1IIlllI = ll1I1IIllII1
            if IlI1l1IIlllI == ll1I1IIllII1:
                if not Il1II1l1Ill1.lII1I1II1I1l(I11lIll11lII):
                    IlI1l1IIlllI = ll1lllIlll1l
                else:
                    IlI1l1IIlllI = ll1llll111Il
            if IlI1l1IIlllI == ll111Ill1Il1:
                IIIIll1Illll = lI1llllIll1I
            if IlI1l1IIlllI == ll1lllIlll1l:
                IIIIll1Illll = IlllIIl1111I
            if IIIIll1Illll == lI1llllIll1I:
                ll11II111l1l = IlllIIl1111I
                if not ll1Ill1l1II1lIII11(l11lll11I11l_other_47990, Promise):
                    ll11II111l1l = l1IIIl1lII11
                else:
                    ll11II111l1l = l11IIIllIl1l
                if ll11II111l1l == Ill1lll1I1l1:
                    if not lIl1Il11I11I(I11l111IlIIl):
                        ll11II111l1l = l1IIIl1lII11
                    else:
                        ll11II111l1l = l11Il11lIIlI
                if ll11II111l1l == l11Il11lIIlI:
                    IIIIll1Illll = IlllIIl1111I
                if ll11II111l1l == IIIII1llIl1l:
                    IIIIll1Illll = l11l11l11Ill
            if IIIIll1Illll == l11l11l11Ill:
                pass
            if IIIIll1Illll == IIlIIIllll1l:
                l11lll11I11l_other_47990 = l11lll11I11l_other_47990.__cast()
            return not l1llII1lII1I(llI1IlIllll1_self_92158.__cast(), l11lll11I11l_other_47990)

        def __le__(self, other):
            (lll11lll1Ill_self_40440, llIl1l11lIII_other_67187) = (self, other)
            I111IlllI11I = Il1l1I1III1I
            III11lI1lI1l = lI1l11lI1l11
            if not l1llII1lII1I(I1IlIIIlllII, l11Illl1IllI):
                III11lI1lI1l = IIIll1lI11ll
            else:
                III11lI1lI1l = I11lI1lIII1l
            if III11lI1lI1l == I1I1IllI1Il1:
                if not llI1llIIlllI:
                    III11lI1lI1l = I11lI1lIII1l
                else:
                    III11lI1lI1l = ll1l1lIll1l1
            if III11lI1lI1l == lIIIIIIl1IIl:
                I111IlllI11I = IllIll1IlIll
            if III11lI1lI1l == I11lI1lIII1l:
                I111IlllI11I = l1I11llI11Il
            if I111IlllI11I == IlIIII111l1I:
                IIlIl11IIlI1 = IlIl1I111I11
                if not llllII1llI1I(llIl1l11lIII_other_67187, Promise):
                    IIlIl11IIlI1 = lII1111l111l
                else:
                    IIlIl11IIlI1 = IllI1111I1I1
                if IIlIl11IIlI1 == lIlII1l1lIl1:
                    if not lll11IIl1I1l:
                        IIlIl11IIlI1 = llI1llIIlllI
                    else:
                        IIlIl11IIlI1 = IlllllII1lIl
                if IIlIl11IIlI1 == IlllllII1lIl:
                    I111IlllI11I = I1lI1lI1ll11
                if IIlIl11IIlI1 == I11Il1llI11I:
                    I111IlllI11I = l1I11llI11Il
            if I111IlllI11I == lI1lIl1I1IIl:
                llIl1l11lIII_other_67187 = llIl1l11lIII_other_67187.__cast()
            if I111IlllI11I == l1I11llI11Il:
                pass
            return not l1I111lll1II(lll11lll1Ill_self_40440.__cast(), llIl1l11lIII_other_67187)

        def __gt__(self, other):
            (IIllIIlIlI1I_self_54119, IIlII1llIlI1_other_51785) = (self, other)
            lI1II1Il11l1 = IIIll1lI11ll
            l1llI11IIIl1 = lI11Il111III
            if not l1ll1IllIlll(I1lI1llIll11):
                l1llI11IIIl1 = lI1111lI11l1
            else:
                l1llI11IIIl1 = I1Il11Ill1Il
            if l1llI11IIIl1 == I1Il11Ill1Il:
                if not lIIIIllIII1I(IIlII1llIlI1_other_51785, Promise):
                    l1llI11IIIl1 = lIlII1IlI1Il
                else:
                    l1llI11IIIl1 = ll1111II1I11
            if l1llI11IIIl1 == l1II1I1Il1ll:
                lI1II1Il11l1 = IIIIIll1llII
            if l1llI11IIIl1 == l1I111ll1llI:
                lI1II1Il11l1 = Il111ll11lII
            if lI1II1Il11l1 == l1llIIll1III:
                ll11Il1Ill1l = IlllllII1lIl
                if not lIl1Il11I11I(lIl1I1llll1I):
                    ll11Il1Ill1l = l11lll1lllII
                else:
                    ll11Il1Ill1l = lI1II1l111I1
                if ll11Il1Ill1l == II1lIllIll1l:
                    if not lIl1Il11I11I(IlIl1I111I11):
                        ll11Il1Ill1l = l1Il1I111l1l
                    else:
                        ll11Il1Ill1l = l11lll1lllII
                if ll11Il1Ill1l == lllIll1l111l:
                    lI1II1Il11l1 = lI11III1ll1l
                if ll11Il1Ill1l == IIll1Il1Il1I:
                    lI1II1Il11l1 = IIIIIll1llII
            if lI1II1Il11l1 == lI11III1ll1l:
                pass
            if lI1II1Il11l1 == l11l11l11Ill:
                IIlII1llIlI1_other_51785 = IIlII1llIlI1_other_51785.__cast()
            return not Il111IllIlII(IIllIIlIlI1I_self_54119.__cast(), IIlII1llIlI1_other_51785)

        def __ge__(self, other):
            (I11III1111ll_other_79840, lI11l1Ill1ll_self_84784) = (other, self)
            llIl1IIll1Il = llIll1l11III
            lIl1IllIll1l = llI1IlIIl11I
            if not llllII1llI1I(I11III1111ll_other_79840, Promise):
                lIl1IllIll1l = l11IIl1IIllI
            else:
                lIl1IllIll1l = ll1Il1I1Il1I
            if lIl1IllIll1l == I1l1lllIlII1:
                if not IIl11l1111ll:
                    lIl1IllIll1l = Il11llI1llII
                else:
                    lIl1IllIll1l = l1l1I1IIl1l1
            if lIl1IllIll1l == l11IIl1IIllI:
                llIl1IIll1Il = I1II1I1II1I1
            if lIl1IllIll1l == I11l111IlIIl:
                llIl1IIll1Il = I1Il11Ill1Il
            if llIl1IIll1Il == IIlIIllll11l:
                IIIIIl1IIII1 = lIlII1IlI1Il
                if not lIl1Il11I11I(Il11l1lIII11):
                    IIIIIl1IIII1 = l111IIllII11
                else:
                    IIIIIl1IIII1 = IIIllIlIIII1
                if IIIIIl1IIII1 == I1IIIII1I1Il:
                    if Il111IllIlII(l1l11IlII111, l1I11llI11Il):
                        IIIIIl1IIII1 = IlllI1I11I1I
                    else:
                        IIIIIl1IIII1 = l1II1I1Il1ll
                if IIIIIl1IIII1 == I1IlI1Il11ll:
                    llIl1IIll1Il = ll1lllIlll1l
                if IIIIIl1IIII1 == I1111I1IIll1:
                    llIl1IIll1Il = IIIII1llIl1l
            if llIl1IIll1Il == l1IIIl1lII11:
                I11III1111ll_other_79840 = I11III1111ll_other_79840.__cast()
            if llIl1IIll1Il == I1II1I1II1I1:
                pass
            return not Illlll111lIl(lI11l1Ill1ll_self_84784.__cast(), I11III1111ll_other_79840)

        def __hash__(self):
            IIIl11I111Il_self_18308 = self
            return I1IIII11I1Il(IIIl11I111Il_self_18308.__cast())

        def __format__(self, format_spec):
            (IIIlI1lll1I1_format_spec_48961, I111lIIIII1l_self_71354) = (format_spec, self)
            return l11111l111lI(I111lIIIII1l_self_71354.__cast(), IIIlI1lll1I1_format_spec_48961)

        def __add__(self, other):
            (l1lI111I1III_self_73616, llI1III1llIl_other_42917) = (self, other)
            return l1lI111I1III_self_73616.__cast() + llI1III1llIl_other_42917

        def __radd__(self, other):
            (III1IllI1l1l_self_40503, I1IlIlII1lll_other_98330) = (self, other)
            return I1IlIlII1lll_other_98330 + III1IllI1l1l_self_40503.__cast()

        def __mod__(self, other):
            (IIll1l11II11_other_41880, IIlll1IIlIll_self_3710) = (other, self)
            return IIlll1IIlIll_self_3710.__cast() % IIll1l11II11_other_41880

        def __mul__(self, other):
            (II1lIlI1I11I_self_9046, Il1Il1lIlllI_other_647) = (self, other)
            return II1lIlI1I11I_self_9046.__cast() * Il1Il1lIlllI_other_647
    for lIIlIII1Il11 in lIlIllI111lI(II1lll1l11I1, lII11lIIIIlI):
        if ((II11II11I11I >= lII1II1l111I or l11IIl1IIllI != IIIII11lI1Il) or (not l111IIllII11 and l1ll1IllIlll(lIIllIl1ll1I))) or ((not Il1II1l1Ill1.lII1I1II1I1l(l1I11llIl1II) or not Il1II1l1Ill1.lII1I1II1I1l(lIIllIl1ll1I)) or (not l1ll1IllIlll(lI11Il111III) or not IIIllIlIIII1)):
            while (lIIIlIl11II1 >= l11IIl1IIllI and (not l1ll1IllIlll(II11II11I11I)) or (not l1ll1IllIlll(lIll11IlII1I) and llIII1II1lII <= I11l111IlIIl)) or ((lIl1Il11I11I(lllllIlIII1I) or not l1ll1IllIlll(lllllIlIII1I)) and (IlIlll11I1lI and l1I11llI11Il)):
                while ((I1l11ll1IIll == ll1Il1I1Il1I or lI1II1l111I1 < I1ll1lIlIllI) or (l1ll1IllIlll(IlIllllI11Il) and (not lIl1Il11I11I(II11Il1111ll)))) and (Il111ll11lII and l1ll1IllIlll(IlI1lI1lI1Il) or (not II11II11I11I and I1lI1lI1IIII >= ll111lllI11l)):
                    if ((l11lI1lllll1 and l1ll1IllIlll(II1I11l11lI1)) and (lIIllIl1ll1I == IlIIIlIlIllI or not l1ll1IllIlll(I1lI1lllIIll))) and ((not lI1IIIl11lll or I1lll111IIll) and (I1IlI1Il11ll == lI111Il1lII1 or not II1lll1l11I1)):
                        for lIIl111l11Il_resultclass_42290 in lI11llI1Il1l_resultclasses_59483:
                            ll1llIIlI1l1 = IIIIIIl11IIl
                            I11I1Ill1IIl = I11Il1llI11I
                            I1Ill1IlllII = IllI1lI1lI1I
                            lIlIllIlI1ll = IIlII1lI111I
                            II1l1lIlII1I = l1I1ll111III
                            if not lIl1Il11I11I(Il1I1111ll11):
                                II1l1lIlII1I = lI1lIl1llIIl
                            else:
                                II1l1lIlII1I = l1I1ll1lII1l
                            if II1l1lIlII1I == I11Illl1lIII:
                                if not l1ll1IllIlll(I1IlIIl1llIl):
                                    II1l1lIlII1I = l1IIIlIll1l1
                                else:
                                    II1l1lIlII1I = I1IlIIIlllII
                            if II1l1lIlII1I == lI1lIl1llIIl:
                                lIlIllIlI1ll = I11lIll11lII
                            if II1l1lIlII1I == lI1llllIll1I:
                                lIlIllIlI1ll = ll111Ill1Il1
                            if lIlIllIlI1ll == I11IIl1l11l1:
                                l11IIlllIlIl = IIIll1lllIII
                                if not Ill1lIll11II(II11II11I11I, II11II11I11I):
                                    l11IIlllIlIl = l1Il1111l1II
                                else:
                                    l11IIlllIlIl = l111I1I1I1lI
                                if l11IIlllIlIl == ll1Il11ll11l:
                                    if not l1ll1IllIlll(lllllIlIII1I):
                                        l11IIlllIlIl = l111I1I1I1lI
                                    else:
                                        l11IIlllIlIl = llIlIl1lIlIl
                                if l11IIlllIlIl == l111I1I1I1lI:
                                    lIlIllIlI1ll = lllllIIlIII1
                                if l11IIlllIlIl == llIlIl1lIlIl:
                                    lIlIllIlI1ll = IIIlIl11II1I
                            if lIlIllIlI1ll == lII11IlIIl11:
                                I1Ill1IlllII = I1lllIIl11Il
                            if lIlIllIlI1ll == ll1llll111Il:
                                I1Ill1IlllII = I111111I1IIl
                            if I1Ill1IlllII == II11II11I11I:
                                ll1II1I1lIII = l1IIIl1lII11
                                Il1IIl11IIl1 = I1III1IIl1Il
                                if not Illlll111lIl(IlIIl1IlIlII, Il1l1I1III1I):
                                    Il1IIl11IIl1 = IIl11I1IllII
                                else:
                                    Il1IIl11IIl1 = l1IIlIllI11I
                                if Il1IIl11IIl1 == Il111l11l1ll:
                                    if not Il1II1l1Ill1.lII1I1II1I1l(lIlII1l1lIl1):
                                        Il1IIl11IIl1 = ll1I1lIIIlII
                                    else:
                                        Il1IIl11IIl1 = lIl1IlII11Il
                                if Il1IIl11IIl1 == lIl1IlII11Il:
                                    ll1II1I1lIII = l1l1I1IIl1l1
                                if Il1IIl11IIl1 == ll1ll1II1l1:
                                    ll1II1I1lIII = I111111I1IIl
                                if ll1II1I1lIII == llIlIl1IllII:
                                    lI1I1IlI1l11 = llIlIl1lIlIl
                                    if not l1ll1IllIlll(IIl11l1111ll):
                                        lI1I1IlI1l11 = IIl11l1111ll
                                    else:
                                        lI1I1IlI1l11 = I11IlI1111I1
                                    if lI1I1IlI1l11 == IIl11l1111ll:
                                        if not l1ll1IllIlll(l11Il11lIIlI):
                                            lI1I1IlI1l11 = I11IlI1111I1
                                        else:
                                            lI1I1IlI1l11 = III1II1II1II
                                    if lI1I1IlI1l11 == lll11IIl1I1l:
                                        ll1II1I1lIII = lllI11lIl1I1
                                    if lI1I1IlI1l11 == I11l111IlIIl:
                                        ll1II1I1lIII = l1I1I11IlllI
                                if ll1II1I1lIII == I11IIl1l11l1:
                                    I1Ill1IlllII = llIlIl1IllII
                                if ll1II1I1lIII == II1lIllIll1l:
                                    I1Ill1IlllII = I1IlIIIlllII
                            if I1Ill1IlllII == lIl1I111l111:
                                I11I1Ill1IIl = Il111l11l1ll
                            if I1Ill1IlllII == llIlIl1IllII:
                                I11I1Ill1IIl = IIIlIl11II1I
                            if I11I1Ill1IIl == Il111l11l1ll:
                                if not lIl1Il11I11I(ll1I1IIllII1):
                                    I11I1Ill1IIl = IIIlIl11II1I
                                else:
                                    I11I1Ill1IIl = ll1I11Il1lI1
                            if I11I1Ill1IIl == lI1II1l111I1:
                                ll1llIIlI1l1 = lII1l11II1lI
                            if I11I1Ill1IIl == ll1l11Il11Il:
                                ll1llIIlI1l1 = Il111l11l1ll
                            if ll1llIIlI1l1 == I1lllIIII1I1:
                                lI1III11lll1 = lIl11l1ll1II
                                if not Illlll111lIl(lIl11l1ll1II, I111l11lIlIl):
                                    lI1III11lll1 = ll1IlllII11I
                                else:
                                    lI1III11lll1 = l1Ill111l111
                                if lI1III11lll1 == l1Il1lI1l1ll:
                                    if not lIl1Il11I11I(II11Il1111ll):
                                        lI1III11lll1 = llI1IIllI1lI
                                    else:
                                        lI1III11lll1 = llllI1I11lIl
                                if lI1III11lll1 == ll1IlllII11I:
                                    ll1llIIlI1l1 = Il111l11l1ll
                                if lI1III11lll1 == l1IIIlIll1l1:
                                    ll1llIIlI1l1 = Il11II1I1ll1
                            if ll1llIIlI1l1 == IIl11I1IllII:
                                for lI11l1IlII1I_type__4817 in lIIl111l11Il_resultclass_42290.mro():
                                    lIIlll1II1lI = Il111lI1Il1l
                                    I1Ill111IIll = IIIlll1ll111
                                    if not ll1Il11ll11l:
                                        I1Ill111IIll = lll11IIl1I1l
                                    else:
                                        I1Ill111IIll = lI1lll1lI1Il
                                    if I1Ill111IIll == I1IIIII1I1Il:
                                        if Il111IllIlII(lIIlll1l1l1l, l1lIlI1Ill11):
                                            I1Ill111IIll = lI1lIl1llIIl
                                        else:
                                            I1Ill111IIll = l1Il1111I1l1
                                    if I1Ill111IIll == l1Il1111I1l1:
                                        lIIlll1II1lI = IIlIIIllll1l
                                    if I1Ill111IIll == lIl1I111l111:
                                        lIIlll1II1lI = l11IIl1IIllI
                                    if lIIlll1II1lI == Il1I1111ll11:
                                        l11l11I1I1lI = IIIlIl11II1I
                                        lIl1lI11I11l = I1l1lllIlII1
                                        I11l1lIIll11 = I1lI1llIll11
                                        l11IIIlIlllI = IlII111III1I
                                        if l1llII1lII1I(IIl111ll1I1I, l11lII11llll):
                                            l11IIIlIlllI = lII1111l111l
                                        else:
                                            l11IIIlIlllI = l11lI1lllll1
                                        if l11IIIlIlllI == l1II1I1Il1ll:
                                            if l1llII1lII1I(II1lI11IllIl, l1l1I1IIl1l1):
                                                l11IIIlIlllI = l1Il1IIIII1l
                                            else:
                                                l11IIIlIlllI = l11lI1lllll1
                                        if l11IIIlIlllI == l11lI1lllll1:
                                            I11l1lIIll11 = IIIIIIl11IIl
                                        if l11IIIlIlllI == l1Il1IIIII1l:
                                            I11l1lIIll11 = lI1l1III111I
                                        if I11l1lIIll11 == lIIIIIIl1IIl:
                                            Ill1I1I11IlI = lIlII1l1lIl1
                                            if not lIl1Il11I11I(II1IIlIl1lIl):
                                                Ill1I1I11IlI = IIIll1lI11ll
                                            else:
                                                Ill1I1I11IlI = lI1111lI11l1
                                            if Ill1I1I11IlI == IlIlll11I1lI:
                                                if not I1IIl1lIl111:
                                                    Ill1I1I11IlI = IIl1ll1lll11
                                                else:
                                                    Ill1I1I11IlI = IIIll1lI11ll
                                            if Ill1I1I11IlI == lII1l11II1lI:
                                                I11l1lIIll11 = lI1llllIll1I
                                            if Ill1I1I11IlI == lI11III1ll1l:
                                                I11l1lIIll11 = IlI1lI1lI1Il
                                        if I11l1lIIll11 == lI11llIl1l1l:
                                            lIl1lI11I11l = ll1lI1I1Il1l
                                        if I11l1lIIll11 == l1IIIlIll1l1:
                                            lIl1lI11I11l = I11ll11lll1l
                                        if lIl1lI11I11l == ll1lI1I1Il1l:
                                            II1I1l1I11ll = IlIIII111l1I
                                            l1IlI1ll1lll = lI1IIIl11lll
                                            if not lIl1Il11I11I(ll111lllI11l):
                                                l1IlI1ll1lll = Illl1ll1l1lI
                                            else:
                                                l1IlI1ll1lll = I1IlI1Il11ll
                                            if l1IlI1ll1lll == Il111lI1Il1l:
                                                if ll1ll11l1IIl(IIl11I1IllII, IIl11I1IllII):
                                                    l1IlI1ll1lll = llllI1I11lIl
                                                else:
                                                    l1IlI1ll1lll = l1l1l11IlI11
                                            if l1IlI1ll1lll == lI1llllIll1I:
                                                II1I1l1I11ll = I1IlIIIlllII
                                            if l1IlI1ll1lll == ll1Il1I1Il1I:
                                                II1I1l1I11ll = ll1l1lIll1l1
                                            if II1I1l1I11ll == lIIIIIIl1IIl:
                                                I1lI1ll1Illl = ll1Il11ll11l
                                                if not l1ll1IllIlll(II11Il1111ll):
                                                    I1lI1ll1Illl = llIlI1I1111l
                                                else:
                                                    I1lI1ll1Illl = llII1IIlI11I
                                                if I1lI1ll1Illl == l1I11llI11Il:
                                                    if not lIl1Il11I11I(l1Illl111l1l):
                                                        I1lI1ll1Illl = llII1IIlI11I
                                                    else:
                                                        I1lI1ll1Illl = lIIllIl1ll1I
                                                if I1lI1ll1Illl == IlII111III1I:
                                                    II1I1l1I11ll = llIlI11Ill1I
                                                if I1lI1ll1Illl == lllllIlIII1I:
                                                    II1I1l1I11ll = lI1lIl1llIIl
                                            if II1I1l1I11ll == l1I1ll111III:
                                                lIl1lI11I11l = l11lIIIllI11
                                            if II1I1l1I11ll == lIl1I111l111:
                                                lIl1lI11I11l = l11111IlIIl1
                                        if lIl1lI11I11l == I1lI1lI1ll11:
                                            l11l11I1I1lI = I11Illl1lIII
                                        if lIl1lI11I11l == llII1IIlI11I:
                                            l11l11I1I1lI = I1IIl1lIl111
                                        if l11l11I1I1lI == I11Illl1lIII:
                                            if l1I111lll1II(IlII1lI1Il11, l1llIIll1III):
                                                l11l11I1I1lI = lllllIlIII1I
                                            else:
                                                l11l11I1I1lI = llIlI1I1111l
                                        if l11l11I1I1lI == l11lIIIllI11:
                                            lIIlll1II1lI = l1llIIlI1l1I
                                        if l11l11I1I1lI == II1l1I1IIIl1:
                                            lIIlll1II1lI = lI1l11lI1l11
                                    if lIIlll1II1lI == Il11llI1llII:
                                        pass
                                    if lIIlll1II1lI == lI1l11lI1l11:
                                        for I111I1llII11 in lIlIllI111lI(lII1Ill1II1l, llIll1l11III):
                                            for lll1l1llIIll_method_name_66838 in lI11l1IlII1I_type__4817.__dict__:
                                                II1lIl1l11lI = IllIll1IlIll
                                                II11Ill1I1l1 = lI1ll11I11Il
                                                if not Il1II1l1Ill1.lII1I1II1I1l(Il1IlI1111ll):
                                                    II11Ill1I1l1 = IllI1111I1I1
                                                else:
                                                    II11Ill1I1l1 = Il11Il11lllI
                                                if II11Ill1I1l1 == ll1I1IIllII1:
                                                    if not l11lIl1IIl1I:
                                                        II11Ill1I1l1 = IIIllI1l1I1I
                                                    else:
                                                        II11Ill1I1l1 = l1l1l11IlI11
                                                if II11Ill1I1l1 == lllllIIlIII1:
                                                    II1lIl1l11lI = II1lll1l11I1
                                                if II11Ill1I1l1 == l1l1l11IlI11:
                                                    II1lIl1l11lI = lI11llIl1l1l
                                                if II1lIl1l11lI == Ill111l1lII1:
                                                    llI1llIIIl1l = l11Il11lIIlI
                                                    if not Il111IllIlII(l1Il1111l1II, Il111lIII1Il):
                                                        llI1llIIIl1l = III111Illl1l
                                                    else:
                                                        llI1llIIIl1l = l1l1I1IIl1l1
                                                    if llI1llIIIl1l == l1l1I1IIl1l1:
                                                        IllIl111I1lI = l1I1ll1lII1l
                                                        I1II1I11Il1l = l1IlllIIIlII
                                                        l1lIIII1ll11 = lIII11lIIl1l
                                                        if not Il1II1l1Ill1.lII1I1II1I1l(I1ll1lIlIllI):
                                                            l1lIIII1ll11 = l11lI1111llI
                                                        else:
                                                            l1lIIII1ll11 = I1Il11Ill1Il
                                                        if l1lIIII1ll11 == I1II11llI111:
                                                            if not III111Illl1l:
                                                                l1lIIII1ll11 = l11lIl1IIl1I
                                                            else:
                                                                l1lIIII1ll11 = ll1IIlII1l1I
                                                        if l1lIIII1ll11 == Il11I1I1II1l:
                                                            I1II1I11Il1l = IIlIIllll11l
                                                        if l1lIIII1ll11 == Ill11llll11I:
                                                            I1II1I11Il1l = l11lIIIllI11
                                                        if I1II1I11Il1l == l11lIIIllI11:
                                                            III1I1l1III1 = ll1lI1I1Il1l
                                                            if not I1lI1lI1ll11:
                                                                III1I1l1III1 = ll1lllIlll1l
                                                            else:
                                                                III1I1l1III1 = IIlII1lI111I
                                                            if III1I1l1III1 == l11111IlIIl1:
                                                                if not II1l1ll11l1l:
                                                                    III1I1l1III1 = ll1lllIlll1l
                                                                else:
                                                                    III1I1l1III1 = llIII1II1lII
                                                            if III1I1l1III1 == lIII11lIIl1l:
                                                                I1II1I11Il1l = II1l11llI111
                                                            if III1I1l1III1 == l1IIIlIll1l1:
                                                                I1II1I11Il1l = I1Il11Ill1Il
                                                        if I1II1I11Il1l == IIlIIllll11l:
                                                            IllIl111I1lI = l1llIIlI1l1I
                                                        if I1II1I11Il1l == lI11lIlll1I1:
                                                            IllIl111I1lI = IIlI1l1IlIl1
                                                        if IllIl111I1lI == l1llIIlI1l1I:
                                                            lll11l1IllI1 = l1Il1I111l1l
                                                            II1ll11IIl11 = I1III1IIl1Il
                                                            if not lIlII1l1lIl1:
                                                                II1ll11IIl11 = I1I11ll1I11I
                                                            else:
                                                                II1ll11IIl11 = lI1ll11I11Il
                                                            if II1ll11IIl11 == lI1lIl1I1IIl:
                                                                if not llI1IlIIl11I:
                                                                    II1ll11IIl11 = I1lI1l111lII
                                                                else:
                                                                    II1ll11IIl11 = lIl1l111I11l
                                                            if II1ll11IIl11 == l1I1ll111III:
                                                                lll11l1IllI1 = IlI1lI1lI1Il
                                                            if II1ll11IIl11 == I1lll1l11l1l:
                                                                lll11l1IllI1 = IIl11I1IllII
                                                            if lll11l1IllI1 == lI1l1III111I:
                                                                l111Il111I1l = I1IlI1Il11ll
                                                                if not l1llII1lII1I(l1Il1111l1II, lIIll11I1IIl):
                                                                    l111Il111I1l = lI1llllIll1I
                                                                else:
                                                                    l111Il111I1l = Il111ll11lII
                                                                if l111Il111I1l == l1IlllII1I1I:
                                                                    if not l1ll1IllIlll(I1III1IIl1Il):
                                                                        l111Il111I1l = Ill1I11Ill11
                                                                    else:
                                                                        l111Il111I1l = I1Il11Ill1Il
                                                                if l111Il111I1l == llIlIl1lIlIl:
                                                                    lll11l1IllI1 = IIl11I1IllII
                                                                if l111Il111I1l == lI1llllIll1I:
                                                                    lll11l1IllI1 = lII1Ill1II1l
                                                            if lll11l1IllI1 == I1lI1llIll11:
                                                                IllIl111I1lI = Il111ll11lII
                                                            if lll11l1IllI1 == Il111l11l1ll:
                                                                IllIl111I1lI = IIlI1l1IlIl1
                                                        if IllIl111I1lI == IIlI1l1IlIl1:
                                                            llI1llIIIl1l = lII1lllll1II
                                                        if IllIl111I1lI == IIIlII11ll1I:
                                                            llI1llIIIl1l = IIIIIIl11IIl
                                                    if llI1llIIIl1l == IIIIIIl11IIl:
                                                        II1lIl1l11lI = IlI1lI1lI1Il
                                                    if llI1llIIIl1l == I11I1lIllIl1:
                                                        II1lIl1l11lI = Il1II1I1I11l
                                                if II1lIl1l11lI == I11IIl1IIIII:
                                                    pass
                                                if II1lIl1l11lI == IlI1lI1lI1Il:
                                                    lll11IlI1IlI = lIl1lIllI1l1
                                                    lI11lllllllI = I11l111IlIIl
                                                    if not l1ll1IllIlll(l1II1I1Il1ll):
                                                        lI11lllllllI = ll11IllI11II
                                                    else:
                                                        lI11lllllllI = lIlII1l1lIl1
                                                    if lI11lllllllI == IlllIIl1111I:
                                                        if Ill1lIll11II(l11IIIllIl1l, I1lII1Il1lI1):
                                                            lI11lllllllI = Il1II1I1I11l
                                                        else:
                                                            lI11lllllllI = lIlII1l1lIl1
                                                    if lI11lllllllI == Il11llI1llII:
                                                        lll11IlI1IlI = I1Il11Ill1Il
                                                    if lI11lllllllI == lIlII1l1lIl1:
                                                        lll11IlI1IlI = l11Il11lIIlI
                                                    if lll11IlI1IlI == l1Illl111l1l:
                                                        l11IIIIIllI1 = II1IIl1lIIIl
                                                        if not l1llllIl1Il1(__proxy__, lll1l1llIIll_method_name_66838):
                                                            l11IIIIIllI1 = IIl11I1IllII
                                                        else:
                                                            l11IIIIIllI1 = IlIIlIIlI1l1
                                                        if l11IIIIIllI1 == IIl11I1IllII:
                                                            if not lIl1Il11I11I(l1Il1111I1l1):
                                                                l11IIIIIllI1 = lI1lII11llll
                                                            else:
                                                                l11IIIIIllI1 = I1IIl111III1
                                                        if l11IIIIIllI1 == lI1lII11llll:
                                                            lll11IlI1IlI = IIl1ll1lll11
                                                        if l11IIIIIllI1 == Ill1lll1I1l1:
                                                            lll11IlI1IlI = I1Il11Ill1Il
                                                    if lll11IlI1IlI == I1Il11Ill1Il:
                                                        pass
                                                    if lll11IlI1IlI == lI11III1ll1l:
                                                        continue

                                                    def __wrapper__(self, *args, __method_name=lll1l1llIIll_method_name_66838, **kw):
                                                        (lI1lI1lI1l1l___method_name_43685, lIll1lIl1Ill_args_95013, II1II1IllIIl_self_32453, IIl11lI11lI1_kw_5464) = (__method_name, args, self, kw)
                                                        II1l11l1II1I_result_43064 = IlIIlIlIIlII_func_65662(*II1II1IllIIl_self_32453._args, **II1II1IllIIl_self_32453._kw)
                                                        return IIllI1llIlIl(II1l11l1II1I_result_43064, lI1lI1lI1l1l___method_name_43685)(*lIll1lIl1Ill_args_95013, **IIl11lI11lI1_kw_5464)
                                                    IIIIIIIllIll(__proxy__, lll1l1llIIll_method_name_66838, __wrapper__)
                            if ll1llIIlI1l1 == ll1Il11ll11l:
                                pass
                    break
                break

    @wraps(IlIIlIlIIlII_func_65662)
    def __wrapper__(*args, **kw):
        (l1I1I111I1II_kw_55477, Il1lIlllll1I_args_17352) = (kw, args)
        return __proxy__(Il1lIlllll1I_args_17352, l1I1I111I1II_kw_55477)
    return __wrapper__

def lazy(func, *resultclasses):
    return IlIl1I111lI1(func, *resultclasses)

def Ill1lllI1III(I1II111lII11_func_27022, l1IIlIIlII1l_kwargs_13228, I11llllllI1I_args_8443, *II1IIl11lll1_resultclasses_29606):
    return lazy(I1II111lII11_func_27022, *II1IIl11lll1_resultclasses_29606)(*I11llllllI1I_args_8443, **l1IIlIIlII1l_kwargs_13228)

def _lazy_proxy_unpickle(func, args, kwargs, *resultclasses):
    return Ill1lllI1III(func, kwargs, args, *resultclasses)

def I111I111IIl1(llI1I1IllI1l_text_48033):
    return lazy(ll1I1l1I1111, lIIIlI11lIl1)(llI1I1IllI1l_text_48033)

def lazystr(text):
    return I111I111IIl1(text)

def l111I1Il1I1I():
    assert not ll1ll11l1IIl(lazystr(I1II1IIlI1Il), IlI1Il1IlIll)

def test_temp():
    return l111I1Il1I1I()

def lIII1l11l1Il(llIllIlI1111_config_string_33858):
    I111ll1llI1l_color_settings_10584 = l1Il1lI1l1ll
    for I1Illlll11I1 in (IlIIII111l1I,):
        for l1lI1ll111I1 in (I1IIl1lIl111,):
            for IlI11I1111lI_role_10838 in [lI1IIIllll11]:
                II1lI111I1l1 = I1I1l111ll1I
                IIlIII1ll1l1 = l1ll1IIlIlII
                l1ll1I1IIllI = IIl11I1IllII
                lllII1l111I1 = lI1lIl1llIIl
                lIIl1l1IIl1I = ll11IllI11II
                if not Il1II1l1Ill1.lII1I1II1I1l(l1l1l11IlI11):
                    lIIl1l1IIl1I = l1l1ll1ll1I1
                else:
                    lIIl1l1IIl1I = I1lI1l111lII
                if lIIl1l1IIl1I == llIlI11Ill1I:
                    if not lIl1Il11I11I(Il1l1I1III1I):
                        lIIl1l1IIl1I = ll1IIlII1l1I
                    else:
                        lIIl1l1IIl1I = lIll11IlII1I
                if lIIl1l1IIl1I == l1l1ll1ll1I1:
                    lllII1l111I1 = l1I1ll111III
                if lIIl1l1IIl1I == ll1IIlII1l1I:
                    lllII1l111I1 = I1l1IllIII11
                if lllII1l111I1 == l1I1ll111III:
                    ll1IIl1IIl1I = ll1I1II111II
                    if not l1ll1IllIlll(I1III1IIl1Il):
                        ll1IIl1IIl1I = llIII1II1lII
                    else:
                        ll1IIl1IIl1I = ll1l11Il11Il
                    if ll1IIl1IIl1I == ll1llll111Il:
                        if Il111IllIlII(l1I1ll1lII1l, lIlII1l1lIl1):
                            ll1IIl1IIl1I = I1lIl1l1l11I
                        else:
                            ll1IIl1IIl1I = l1II1I1Il1ll
                    if ll1IIl1IIl1I == l1II1I1Il1ll:
                        lllII1l111I1 = ll1ll1II1l1
                    if ll1IIl1IIl1I == I1lIl1l1l11I:
                        lllII1l111I1 = I11IlI1111I1
                if lllII1l111I1 == I1l1IllIII11:
                    l1ll1I1IIllI = IlllI1I11I1I
                if lllII1l111I1 == I11IlI1111I1:
                    l1ll1I1IIllI = lI11llIl1l1l
                if l1ll1I1IIllI == lI1l1III111I:
                    lIl1Il1l1ll1 = l1IIIlIll1l1
                    ll1IIIlllI11 = lllIl11I1l1l
                    if not lIlII1l1lIl1:
                        ll1IIIlllI11 = I11l111I11I1
                    else:
                        ll1IIIlllI11 = IIlI1l1IlIl1
                    if ll1IIIlllI11 == I1l1IllIII11:
                        if not l1ll1IllIlll(Il11llI1Il1l):
                            ll1IIIlllI11 = l11l1II11l1l
                        else:
                            ll1IIIlllI11 = I11I1lIllIl1
                    if ll1IIIlllI11 == IllI1111I1I1:
                        lIl1Il1l1ll1 = lllI11lIl1I1
                    if ll1IIIlllI11 == I11l111I11I1:
                        lIl1Il1l1ll1 = III11lIlllII
                    if lIl1Il1l1ll1 == I11IIIlI1I11:
                        I1ll1IIll1l1 = IlllllII1lIl
                        if not Il1II1l1Ill1.lII1I1II1I1l(lIII11lIIl1l):
                            I1ll1IIll1l1 = IIlII1l1lII1
                        else:
                            I1ll1IIll1l1 = IlIl1I111I11
                        if I1ll1IIll1l1 == lI111III1II1:
                            if not Il1II1l1Ill1.lII1I1II1I1l(ll1lI1I1Il1l):
                                I1ll1IIll1l1 = IlIl1I111I11
                            else:
                                I1ll1IIll1l1 = lI11llIl1l1l
                        if I1ll1IIll1l1 == l1l1ll1ll1I1:
                            lIl1Il1l1ll1 = l11111IlIIl1
                        if I1ll1IIll1l1 == lIl11l1ll1II:
                            lIl1Il1l1ll1 = ll1I11Il1lI1
                    if lIl1Il1l1ll1 == ll1I11Il1lI1:
                        l1ll1I1IIllI = IlllI1I11I1I
                    if lIl1Il1l1ll1 == I1lI1lI1ll11:
                        l1ll1I1IIllI = IIII1IIIlI1I
                if l1ll1I1IIllI == II111I11IIl1:
                    IIlIII1ll1l1 = IIIIIll1llII
                if l1ll1I1IIllI == I1IlI1Il11ll:
                    IIlIII1ll1l1 = I1I1l111ll1I
                if IIlIII1ll1l1 == I1I1l111ll1I:
                    if Il111IllIlII(Il111lI1Il1l, IIl1IIllI111):
                        IIlIII1ll1l1 = IIIIIll1llII
                    else:
                        IIlIII1ll1l1 = lI1lIl1llIIl
                if IIlIII1ll1l1 == l11l11l11Ill:
                    II1lI111I1l1 = l1Il1IIIII1l
                if IIlIII1ll1l1 == I1IlIIIlllII:
                    II1lI111I1l1 = lIIllIl1ll1I
                if II1lI111I1l1 == II11II11I11I:
                    Illll1lll11I = lIll1lIlIIIl
                    if not Il1II1l1Ill1.lII1I1II1I1l(l11ll11lIlII):
                        Illll1lll11I = Ill11llll11I
                    else:
                        Illll1lll11I = I1lI1l111lII
                    if Illll1lll11I == IllI1I1lI1l1:
                        if not I1lI1lI1ll11:
                            Illll1lll11I = llIlI11Ill1I
                        else:
                            Illll1lll11I = lIll1Il1lI11
                    if Illll1lll11I == lI1ll11I11Il:
                        II1lI111I1l1 = llI11IIl1l1l
                    if Illll1lll11I == I1IlIIIlllII:
                        II1lI111I1l1 = lIIllIl1ll1I
                if II1lI111I1l1 == IlII111III1I:
                    ll1I11I11lll = lI1lIl1llIIl
                    I1l1ll1I1I1I = ll1I1II111II
                    if not Il1II1l1Ill1.lII1I1II1I1l(I1lllIIl11Il):
                        I1l1ll1I1I1I = lIIl1II11lII
                    else:
                        I1l1ll1I1I1I = llI1IIllI1lI
                    if I1l1ll1I1I1I == llllI11IIIII:
                        if not lIl1Il11I11I(Il111I1I1I1l):
                            I1l1ll1I1I1I = lI1II1l111I1
                        else:
                            I1l1ll1I1I1I = lII1lllll1II
                    if I1l1ll1I1I1I == I11l111I11I1:
                        ll1I11I11lll = llIIIIlIlIIl
                    if I1l1ll1I1I1I == Il1l1I11lIIl:
                        ll1I11I11lll = IIlIIllll11l
                    if ll1I11I11lll == llII111lIIlI:
                        l1ll1IlIlI11 = I1II1I1II1I1
                        if not Il111IllIlII(I1l1IllIII11, IIII1IllIIlI):
                            l1ll1IlIlI11 = lIIIIlII1lll
                        else:
                            l1ll1IlIlI11 = lIIlIl11Illl
                        if l1ll1IlIlI11 == ll1ll1Il11Il:
                            if not I111ll1llI1l_color_settings_10584:
                                l1ll1IlIlI11 = II1IIl1lIIIl
                            else:
                                l1ll1IlIlI11 = lIIIIlII1lll
                        if l1ll1IlIlI11 == ll1llll1lI1l:
                            ll1I11I11lll = lIIl1II11I1l
                        if l1ll1IlIlI11 == II1IIl1lIIIl:
                            ll1I11I11lll = lI1lI111IIIl
                    if ll1I11I11lll == I1Il11Ill1Il:
                        lIIllI1lII1l_style_func_80574 = lIl1IlII11Il
                    if ll1I11I11lll == lI1l11lI1l11:

                        def lIIllI1lII1l_style_func_80574(x):
                            lI1l111I11I1_x_73158 = x
                            return lI1l111I11I1_x_73158
                    Ill111l1ll11(make_style, IlI11I1111lI_role_10838, lIIllI1lII1l_style_func_80574)
                if II1lI111I1l1 == IIl1llI1I1l1:
                    pass
    return I1Ill1lIIlIl

def make_style(config_string=''):
    return lIII1l11l1Il(config_string)