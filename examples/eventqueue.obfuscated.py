import eventpy.policy
import eventpy.lock as lock
import eventpy.eventdispatcher as eventdispatcher
import eventpy.internal.lockguard as lockguard
import time
(II1IIl1l, llIIl11I, llIII11l, l1II11Il, l1I1I11l, IIII1l11, I1l111l1, IIlI1ll1, lIIlIl11, IIl11ll1, I1IIIIII, Il1l1l1I, IIllIllI, III1ll1l, lI11I1II, I1I11l11, IIIll1II, ll1IIllI, ll111llI, llI1llll, lIlI1l1l, lll1IIlI, llll1lI1, I11I11ll, l1llllII, llllIlIl, IllIl1Il, l1lIll11, Ill1lI11, I1l1lII1, l1IlIl1I, l1III1II, llI11Ill, lIll1I1I, ll1l11II, I1I1IIIl, ll1lll11, l1I111ll, I1lIIlll, llII11II, l11I111I, l111l11I, II1l1ll1, IIIl1I1l, IIl111l1, IlIIIIlI, IlI1IIll, III11l11, Ill1111I, lI1111lI, llIl1Ill, llI11III, lIlllI11, I1llI1Il, IIIlllll, IIll1I1l, Ill11IlI, IIl1II11, IlI1llII, lI1llll1, lI11lllI, Ill1l1lI, lI1ll1l1, lII1I11l, I1I11Il1, lI1I1l1I, lIIIIll1, l111I111, Il1lIl1I, Ill1lIIl, lIlI1I11, II1l1llI, IIIIIllI, I1lII11l, l1l1I1lI, Il111IIl, lIII11l1, ll11lIll, III1IIll, l11ll11I, I1IlIIIl, IIIl1IIl, l1I11Ill, ll1IIll1, I1IlI1Il, I11II11l, lIlIl11I, l1lI1I1l, I1llIllI, IIl1I1I1, IIlll11I, lIl1IIl1, IIII1III, lII11lIl, llI11111, I11111l1, llIIIlll, IIlllI1l, Il1111Il, IlI111I1, l11IlI1I, IllI11Il, IlllIl1l, I1IIlIIl, I11lIlII, Il1l111l, IlIIIl1I, I1llI1II, l1lIlllI, l1IIllI1, IIlllIlI, IIIIIIll, Il11l1II, I1l1Il11, I1l1lIIl, llIII1II, l111llll, IlI11lIl, I11llIl1, IlllI1II, I1l1IIl1, Il11IIlI, II11l1Il, III111lI, Il1lllII, l1Ill11l, IIlIl11I, l1Il1Ill, IlIlI1ll, lI1II1l1, l1I1111l, I1lllll1, I111I1II, I11IIlI1, llIlIlI1, l11l11ll, lIl1l1I1, I1l1111l, Ill1I1lI, Il11I1ll, III111Il, ll1Illl1, ll1I1lll, I1l1lIII, lll11lI1, lllI1I1l, II1I1I1I, IIllI11l, lIII111l, IllI1lI1, I1lIIllI, Illl1llI, IIIllIll, lll1ll1l, lII1IIll, lllll1ll, lII11111, ll1lI1I1, I1l11l11, I1I11I1l, ll1lII1I, lllIII1I, lIlIIl1I, III11I1I, II11IlI1, lIIlll1l, l1IIll11, l1III1Il, I1IlI11l, IlllIl1I, l1lI1l1I, IIllllIl, lll1I1I1, lll1IIl1, lIIIl1l1, I1ll11lI, l111IIIl, lllIIl11, IIIllIlI, lIl11I1I, I111l1I1, l11l11II, l11II1I1, IlllIlIl, I11IIl1l, I1lIlIIl, lIl1IlI1, lll111l1, I1l1IlI1, I1ll1I1I, IlII11I1, ll1IllII, llII11lI, III1I1I1, I11IlIII, IlI1I1ll, llIl11ll, I11lI1l1, ll1I1IlI, IIIlII1l, IIllll11, Ill11l11, l111ll1l, Il11IlI1, IIII1I1I, llIlI11l, IIlllIII, III1ll11, l11llI11, IIlll1lI, ll11II11, I1llI1I1, IIIll111, IlIIII11, lIl1l1ll, I111111l, IlIlIIII, lIIllll1, l11ll1Il, IlIllllI, Il11Illl, lIIlII11, Illll1lI, l1llII11, l111I11l, I1IIlIlI, I1lIllIl, l11I1IIl, l1IIl111, IIllI111, IlI1lI11, llllII1I, II1ll1ll, Il1l11l1, IlllII11, llllI1Il, I1I1I1Il, l1I1IIIl, II1I1IIl, I11l1IIl, llllllll, l11I1III, lIlI1lll, lll11I1I, Il111lI1, Il1I11II, lIlII1ll, lIII1lI1, lIlIlll1, l1I1Ill1, l11I1l11, l11lII1l, l1l1Il11, I1l1ll11, IlIIlll1, I1Ill11l, l111I1Il, l1llI1II, lIl11lIl, l1I1I11I, I1lIII1I, IIllIlII, lII1llIl, lIIIIII1, Il1I1l1I, ll1IlIll, lI11II1I, II1II1I1, I1l1lIlI, l1Ill1lI, Il1I1llI, I1I1III1, Il1lIlIl, I111I1lI, Il111lll, lI1I1l1l, lI11llI1, IIl11I11, I1lIllII, l1III111, I1lIllll, IIlI1III, II1ll1Il, lI11l11l, I11IIlIl, lI1IIlII, lIIllIlI, IllI1IIl, ll1l1I11, lI1IllI1, IllIII11, I1IIII1l, Illl1l11, II1I1ll1, IlllIlII, I1I1111I, lI11l1I1, IIIII111, lIIlI11I, lIllI111, lIlII1l1, IlII1ll1, Il1lIlI1) = ((624520492 ^ 693154553) - (900054794 + -691789667), 760117208 ^ 756429951 ^ 382611993 - 376827475, ~-(964417250 ^ 964417263), 551857533 - -415408396 - (279012621 ^ 688270221), 125756528 ^ 242558110 ^ 129910601 - -21854631, ~(667052375 + -667052408), 219180641 ^ 404852294 ^ 200770475 + 154819721, (554806734 ^ 91438119) + (838974274 + -1449413914), 529216465 + -184696784 - (83662786 ^ 276063291), ~-(389784443 ^ 389784426), 391688379 + 98717673 + (796884963 - 1287290996), 234403166 ^ 261778829 ^ 121273573 - 81241113, ~-979002602 ^ 389645079 - -589357466, ~-~-85, ~-(210475489 ^ 210475509), ~-(983315423 ^ 983315440), ~-487403376 ^ (68279273 ^ 421328017), ~-543555448 ^ (378802557 ^ 921824829), ~-825086151 + -~-825086136, ~-350791433 ^ (907538196 ^ 587155461), 893781643 ^ 505998351 ^ ~-728689291, 170223726 ^ 245563054 ^ 483643582 - 407648731, 449187534 - 128616027 - ~-320571495, (243475064 ^ 698203879) - (249106531 ^ 700943602), ~-925240545 + (635021981 + -1560262509), (766329481 ^ 52263228) - ~-783301541, (537012391 ^ 992810883) - (442072700 ^ 24527012), ~-66109845 ^ (369404304 ^ 368338944), (487577551 ^ 422080481) + -~-69711874, 636167062 ^ 141389723 ^ (512326360 ^ 856635105), 346034724 ^ 474576200 ^ (59220943 ^ 191808641), 134996669 ^ 864970301 ^ (423180293 ^ 582794384), 520277903 - 354075253 + (409628293 - 575830912), ~-(889601391 ^ 889601400), ~-~-28, ~(470333321 - 470333335), (571281793 ^ 562245372) - (344514235 ^ 386326987), 204418390 + 651212090 ^ (168005531 ^ 956067112), 216104723 ^ 620981364 ^ ~-702681931, (279422693 ^ 415407447) + -(234429847 ^ 94119649), (420268337 ^ 156813050) - (841492024 ^ 578562458), (915627730 ^ 467746883) - (592138447 + 170315188), 275370190 ^ 980398478 ^ (405295501 ^ 841887884), 335927549 ^ 778129852 ^ 581253267 + 398414030, ~-(946914918 ^ 946914849), 89655833 ^ 772302948 ^ (11341789 ^ 738028984), None, 735367107 + -21415901 ^ ~-713951179, ~-383252285 ^ 268856503 - -114395777, (384581313 ^ 195553479) + -(135735225 ^ 358412882), 245464137 + 274120658 + (243143107 - 762727884), ~-398619097 - (386044241 + 12574812), 917102880 - 374745490 - (311801140 ^ 851837534), ~-935150193 ^ (603609377 ^ 340204414), 475426959 - -376647089 + -(660652110 ^ 363421299), ~-40822378 ^ ~-40822386, ~-(483993861 ^ 483993890), 960941487 ^ 686655663 ^ ~-296437040, 549870470 ^ 159618123 ^ (722466216 ^ 38419063), ~-(605963841 ^ 605963888), 845963620 ^ 563441619 ^ (884691124 ^ 658660889), (204236060 ^ 296211924) + -(512005241 ^ 51324122), ~-~-24, ~-(538662968 ^ 538662938), ~-90955227 ^ 526393619 + -435438371, ~(490193783 + -490193785), ~-(253110222 ^ 253110270), 162268376 - 84288394 ^ (687921072 ^ 765802210), 0.001, (602179855 ^ 926119287) - (497606109 ^ 159326597), 592539761 ^ 852477145 ^ (496376659 ^ 201895923), 86942442 + 362910379 ^ (770509937 ^ 926759417), ~-(759346579 ^ 759346622), (175169034 ^ 531615401) + -(310935938 ^ 123179272), 103134900 ^ 74920513 ^ ~-38962396, 157016065 ^ 540707246 ^ (854912842 ^ 462784194), 61770341 - -113678106 + (874176326 - 1049624740), 572619775 ^ 356043273 ^ 866273613 - -58157204, 518247229 - 72534818 ^ (168808214 ^ 278841100), (955715896 ^ 651378632) + (315231403 + -820919175), ~(75190773 - 75190792), 685436253 ^ 535436115 ^ (949993846 ^ 263141205), not 7, ~-(692412319 ^ 692412317), 265796653 - -602500484 ^ 565025354 - -303271771, ~-460835686 ^ 591707792 - 130872112, ~-203915776 ^ (286201618 ^ 489199301), 951194518 - 453066745 ^ 278233384 + 219894385, ~-(590267313 ^ 590267316), (138777059 ^ 715383537) - (728417529 + -142889483), 81698424 ^ 344814130 ^ (65688617 ^ 330938441), ~-(486226994 ^ 486226989), 935444355 ^ 688144355 ^ (348991244 ^ 168341373), ~(430448298 + -430448341), 36395011 ^ 15574904 ^ ~-46595933, 179010367 - -5386684 ^ ~-184397049, (400435316 ^ 472000044) - (729929047 ^ 545118997), 874301448 ^ 587272012 ^ (81660287 ^ 331599402), ~-346744075 ^ 29258297 - -317485793, 196255756 + 91787417 - ~-288043173, ~-(656931783 ^ 656931742), (653845733 ^ 197970766) - ~-758394782, 876018916 ^ 26722050 ^ ~-899761149, 633802436 - -184936549 ^ (394726625 ^ 659291093), ~-53868726 ^ 520108893 - 466240196, ~-~-5, 638618266 ^ 347039353 ^ 169684656 + 681754179, 877610926 ^ 214870304 ^ 837431808 - -110607527, (116805565 ^ 343467476) - ~-311339603, 884264370 ^ 1033288349 ^ (344803711 ^ 498024039), ~-404998463 ^ 537672595 - 132674180, ~-577643545 ^ 495313702 - -82329830, 653294924 - -147214703 - (261576386 ^ 539072599), (934995352 ^ 384876298) + (35566033 - 594086981), 603740971 ^ 182537005 ^ (241205133 ^ 662531971), ~-600522968 ^ (504960492 ^ 1037194552), 562568777 + -30280347 ^ 835591021 + -303302636, 843717655 ^ 339202335 ^ 826947247 - 181168558, 94 < 28, 270032917 ^ 311062608 ^ (721367947 ^ 678241276), 10 == 10, 378360113 ^ 288958752 ^ (774180108 ^ 697398564), 264120513 + -105280012 ^ 914465432 - 755624948, ~-~-51, 531176083 + 221586922 ^ 683720224 - -69042774, (261338280 ^ 1042229023) - (932824108 ^ 102062004), (446701988 ^ 164439360) - (990233526 + -664321793), 154349574 + 763712520 ^ (404072220 ^ 783098644), ~-(372158735 ^ 372158723), 230638746 + 74397628 ^ (288279350 ^ 50378571), 584917173 ^ 803073675 ^ 152141811 - -66014772, ~-691291130 - ~-691291084, ~(106223079 - 106223087), ~-(905573005 ^ 905573026), 894206390 ^ 100244416 ^ (304530140 ^ 580114657), 414942144 - -540388107 + -(94896749 ^ 1029254365), ~-(726806465 ^ 726806512), 913513201 + -859378258 ^ 816645217 - 762510295, (132931182 ^ 1063471162) + -~-948901426, 285899621 ^ 635668714 ^ 791567200 + 96180283, 481784650 + 105136074 - (860517745 ^ 296863635), (884148697 ^ 98390700) + -(21809520 ^ 807572003), 714008329 + 213169213 ^ ~-927177572, (523212815 ^ 192886184) + -~-340831626, (116080789 ^ 67405867) + -(436519786 ^ 418057191), 639351594 ^ 330358547 ^ (5330133 ^ 905588937), 492359891 ^ 109129401 ^ ~-467271268, 775999789 - -154210395 ^ 660055161 + 270155085, 71819795 - -202617196 ^ ~-274436980, ~-(932969735 ^ 932969740), 416786860 - -264231422 ^ (448758944 ^ 841484044), ~-(997710041 ^ 997710039), ~-751538325 + -(433539287 ^ 891082845), 331300132 + -286944088 ^ 976969616 + -932613524, (634817584 ^ 578131019) + (150726174 + -278855278), 261413376 ^ 306078405 ^ 707821349 + -210093617, 173918031 + 472254527 - (423834338 ^ 1069612430), 186637185 ^ 274118467 ^ (5283915 ^ 454675629), 532227894 ^ 312801833 ^ (838363003 ^ 1021688396), ~-577153471 ^ (894612974 ^ 389291129), ~-(71705914 ^ 71705892), ~-(830468217 ^ 830468218), 144155864 + 265064611 ^ (979950562 ^ 571272833), 810803893 + -480480566 - (459624884 ^ 148178121), 185026460 - -109509784 ^ (666962457 ^ 911167019), 91517328 - -785657402 ^ 461392242 - -415782493, 601684837 ^ 754001657 ^ (591775834 ^ 745018849), (362321343 ^ 813766029) + -(754148254 ^ 166388635), (622968028 ^ 343881145) - (160826201 + 667452841), 768280663 + 135148897 + (974208282 + -1877637800), (816135430 ^ 195484275) - (964302343 ^ 41546014), (627854357 ^ 511537204) - (414815307 ^ 598255709), 14 == 14, 446270079 ^ 465246506 ^ (504609794 ^ 523317103), 312580706 ^ 900501587 ^ (557117376 ^ 104457667), 817161416 + -677659309 ^ (927708467 ^ 1058740024), (167260921 ^ 654517897) - (729042030 - -59164668), 886326751 ^ 571515061 ^ (452276186 ^ 204589718), ~-~-34, 842695083 ^ 431881014 ^ (129465579 ^ 741344861), 211281818 ^ 585582671 ^ (259047597 ^ 553676663), 234592389 + 289870351 - (159068395 ^ 372873836), 934618398 ^ 489233228 ^ (377694494 ^ 1008670570), (678521634 ^ 296513386) + -(289040878 ^ 686255552), 263793802 ^ 46610643 ^ (380002049 ^ 467159929), 668010850 ^ 487448818 ^ (586943403 ^ 404808252), 712021251 ^ 733188797 ^ 248964378 - 219405703, 288433044 ^ 27031337 ^ (264945431 ^ 526904255), 153976176 - -346151679 ^ (198423357 ^ 370994036), bool(1), 439972175 - -333102437 + (928492563 - 1701567143), 362363153 + 112057541 + (821656875 + -1296077560), ~(898188295 + -898188340), (2078223 ^ 980895857) - (24055285 - -955904037), ~-134516027 ^ 221273856 + -86757836, ~-(524218464 ^ 524218449), ~-969268301 ^ ~-969268329, 834485166 + -702382723 - (231129275 ^ 169441710), (740783683 ^ 668064549) + (220025490 + -420741100), ~-757159828 - (55776112 - -701383620), 414091501 ^ 768728003 ^ ~-897536819, ~-818559593 - ~-818559575, 348268572 ^ 616639093 ^ (917562764 ^ 112453607), (991353695 ^ 897568574) + -~-241767507, 375603244 ^ 37725670 ^ (168671817 ^ 508649388), ~-862152775 + -(19965914 ^ 844353438), ~-163682748 + -~-163682709, 251458291 - -132006354 ^ (213442170 ^ 442755739), 675634534 ^ 60076625 ^ 572561434 + 162617090, 77 > 11, (443417308 ^ 83490339) + -(350244996 ^ 175613025), 742101340 + -251241903 ^ 46937463 - -443921930, 206403483 ^ 577557270 ^ (482938934 ^ 854111388), 23532494 ^ 353353044 ^ ~-342404742, (894111691 ^ 815215832) + -(57972264 ^ 111717599), ~-840070138 - (970124327 - 130054213), 90566192 + 182970482 ^ 848901959 - 575365311, 845353064 ^ 691054621 ^ (477395826 ^ 120046340), 147874909 ^ 225156732 ^ (187468605 ^ 244805933), ~(548788168 + -548788224), ~-228524560 + -~-228524541, 53175451 - -146691346 + -(625023055 ^ 782803433), 244016427 - -244887594 ^ (201812072 ^ 287538443), (489936000 ^ 454680326) + -~-103418731, ~-961448949 ^ (737174363 ^ 314501279), 297493565 ^ 625892176 ^ (664740890 ^ 325720943), 49180808 ^ 370415638 ^ (853774312 ^ 639231863), 189146913 + 75909016 + -(825609740 ^ 1056547007), (223614724 ^ 58593659) + -(280889983 ^ 513018920), 655225822 ^ 215216462 ^ (183830657 ^ 556468741), 876631644 - 179176823 + (316507262 - 1013962069), 201884398 ^ 680098728 ^ (517461160 ^ 978726346), ~(518986656 - 518986677), 574696577 ^ 873241088 ^ 748536160 + -374344365, 893402633 - 744921238 + (136806524 + -285287901), 619064367 ^ 22539678 ^ (691110110 ^ 209731965), ~-192079323 - (614209954 ^ 804191328), ~-81835615 ^ 317293390 - 235457745, ~-355897740 ^ (739863545 ^ 959445588), 55560299 ^ 568436019 ^ 649242424 + -67385828, 334921440 ^ 174035757 ^ 719797991 - 289231133, 630630839 - 442341151 + -(217988047 ^ 130492762), ~-905575858 ^ 940731098 - 35155228, ~-92629175 ^ ~-92629169, 735416011 - 650904256 + (921374182 - 1005885930), 630049515 ^ 46482437 ^ 236823489 + 422243105, (24188187 ^ 390112746) - (767370876 ^ 999069348), 63617909 + 850996210 - (5962715 ^ 920198334), 408877428 - -44503928 + (544001581 + -997382924), 796083338 ^ 86625455 ^ ~-710576162, (313299704 ^ 90672181) - (146043214 ^ 528445434), 603911320 ^ 993533553 ^ 26653807 - -389035636, (181951877 ^ 484905879) + (123851041 - 497098528), 762151552 ^ 806611751 ^ 942216711 - 447392882, (801490509 ^ 916786652) + -(333850164 ^ 176614736), ~-(547675362 ^ 547675380), (762270934 ^ 933945236) - (821772560 ^ 708758065), ~-925067588 + (974273046 + -1899340587), None, (923972500 ^ 303024302) + -(971939975 ^ 485743549), ~-907418270 - (917504564 - 10086304), 95506746 + 119841220 - (835968711 ^ 1023814713), 130525698 - -641168758 + -(790431937 ^ 48371615), 691952694 + -251593409 ^ ~-440359273, 444181362 ^ 1037488087 ^ (83604568 ^ 592761059), ~-621359103 ^ 924900322 + -303541249, 382133957 + 514133828 ^ 545809876 + 350457900, 468712501 + -183756321 + -(994601291 ^ 733248676), (196194874 ^ 600387810) + -(327235170 ^ 1006220468), (233649577 ^ 246026350) - ~-54994375, 686504905 ^ 1017497236 ^ 59290017 - -281430944, ~-268733847 + -(40523017 ^ 309254268), (51522092 ^ 344199897) - ~-395720916, 465491665 ^ 223080780 ^ 569724443 - 184559255, ~-(242396061 ^ 242396048), 756629039 + 184032232 ^ (213116360 ^ 883081214), 97790890 ^ 203362940 ^ (73483397 ^ 229277027), 915617299 + -471163411 - (787493901 ^ 881715157), (5520424 ^ 2806424) + (131941030 + -140259626), 326810695 + 448897114 + -(446615621 ^ 883067933), 420201715 - 33990995 ^ (718657525 ^ 1037093962), ~-(857172902 ^ 857172871), ~-~-12, 376914313 ^ 820371158 ^ 271936667 + 375206572, 939588949 ^ 916328066 ^ ~-245298141, (386064983 ^ 323890652) + -~-72142721, 688050671 - -142193972 ^ 852615644 + -22370998, 604341501 ^ 570407659 ^ 66797787 + 33488225, (801265054 ^ 508309977) - (59462049 + 771953283), 425822791 ^ 741655189 ^ 871762299 + 23019351, (918534609 ^ 275729372) - (137535014 + 513692607), 738157371 + 150024158 - (94255886 ^ 829335558), 665015526 ^ 760226527 ^ (932090335 ^ 1031661549), ~(126500400 + -126500420), ~-(435547081 ^ 435547025), 73206432 + 743294568 ^ ~-816501035, ~(247102740 + -247102806), 7842704 - -950727454 ^ ~-958570166, 258645277 + -107847919 ^ (734185113 ^ 591280774), ~-570330176 ^ (121499889 ^ 650345691), (56254468 ^ 977587763) - (836567551 - -121744406), 575152606 ^ 731324542 ^ 697519886 - 531909947, ~-(607042701 ^ 607042721))

def I111I1Il(lll1l1l1):
    return True

def lllII1II(lll1l1l1):
    return lll1l1l1

class IIlIIIIl:

    @staticmethod
    def I111lIl1(Il1lIIl1):
        return True

    @staticmethod
    def II111lll(Il1lIIl1):
        return Il1lIIl1
ll1lI1lI = lambda I1IIl1Il: True
I1lllIIl = lambda I1IIl1Il: I1IIl1Il

def I1Il1lIl(l1Ill1II, II1lIl1I):
    try:
        return l1Ill1II != II1lIl1I
    except:
        return not l1Ill1II == II1lIl1I

def IIll1I1I(llII111I, Il1l1II1):
    try:
        return llII111I < Il1l1II1
    except:
        return not llII111I >= Il1l1II1

def Il1lI1Il(ll11lI11, IIl1ll11):
    try:
        return ll11lI11 <= IIl1ll11
    except:
        return not ll11lI11 > IIl1ll11

def llII1l1I(I11l1llI, Il1IlIl1):
    try:
        return I11l1llI > Il1IlIl1
    except:
        return not I11l1llI <= Il1IlIl1

def I1IllIll(III1IlI1, Ill1I111):
    try:
        return III1IlI1 == Ill1I111
    except:
        return not III1IlI1 != Ill1I111

def lIlI11ll(I11I1l1I, ll1lIIIl):
    try:
        return I11I1l1I >= ll1lIIIl
    except:
        return not I11I1l1I < ll1lIIIl

def Ill11I1I(II11lIll, lIlIIII1):
    lIlIIII1._queue = II11lIll

def IllI1lIl(lII11l1I):
    lII11l1I._queue._queueNotifyCounter += III1IIll
    return lII11l1I

def l1llIII1(IIl111II, lI1I1Il1, l1l111Il, lll1lIll):
    lI1I1Il1._queue._queueNotifyCounter -= IlI111I1
    l1I11lI1 = llII11lI
    Ill1IIl1 = l11I1III
    if not IIlIIIIl.I111lIl1(Il1l111l):
        Ill1IIl1 = IlllIlIl
    else:
        Ill1IIl1 = Ill11IlI
    if Ill1IIl1 == lllIIl11:
        if not I11IIlIl:
            Ill1IIl1 = ll11II11
        else:
            Ill1IIl1 = I1lIIllI
    if Ill1IIl1 == l1Il1Ill:
        l1I11lI1 = I1l1Il11
    if Ill1IIl1 == IlllIl1l:
        l1I11lI1 = lIl1l1I1
    if l1I11lI1 == I1l1Il11:
        lIlIIl1l = IIl1II11
        lll1Il11 = lIlIlll1
        if not lI1I1Il1._queue._doCanNotifyQueueAvailable():
            lll1Il11 = lI11l11l
        else:
            lll1Il11 = I111I1II
        if lll1Il11 == I111I1II:
            if not lI1I1Il1._queue.emptyQueue():
                lll1Il11 = IllI1IIl
            else:
                lll1Il11 = I1IIlIlI
        if lll1Il11 == IIlll11I:
            lIlIIl1l = lllIII1I
        if lll1Il11 == lI11l11l:
            lIlIIl1l = l1l1I1lI
        if lIlIIl1l == l1llI1II:
            if not ll1lI1lI(I111I1II):
                lIlIIl1l = lllIII1I
            else:
                lIlIIl1l = lII1IIll
        if lIlIIl1l == lIl11I1I:
            l1I11lI1 = lIl1l1I1
        if lIlIIl1l == l111ll1l:
            l1I11lI1 = II1II1I1
    if l1I11lI1 == II1II1I1:
        with lockguard.LockGuard(lI1I1Il1._queue._queueListMutex):
            lI1I1Il1._queue._queueListConditionVariable.notify()
    if l1I11lI1 == l111I11l:
        pass

class DisableQueueNotify:

    def __init__(self, queue):
        return Ill11I1I(queue, self)

    def __enter__(self):
        return IllI1lIl(self)

    def __exit__(self, type, value, traceBack):
        return l1llIII1(value, self, traceBack, type)

def l11lIlIl(I1Il1l11, Ill1lllI, ll1lI1II, ll111lll):
    Ill1lllI.event = I1Il1l11
    Ill1lllI.args = ll1lI1II
    Ill1lllI.kwargs = ll111lll

class QueuedEvent:

    def __init__(self, event, args, kwargs):
        return l11lIlIl(event, self, args, kwargs)

def II1IlI1I(l1l11llI, *Ill1Il1l, **I1I1llll):
    I1IIl1l1 = l1l11llI._policy.getEvent(*Ill1Il1l, **I1I1llll)
    l1l1Illl = II1II1I1
    lll11llI = lllIIl11
    if I1Il1lIl(l1l11llI._policy.argumentPassingMode, eventpy.policy.argumentPassingExcludeEvent):
        lll11llI = llI1llll
    else:
        lll11llI = llllI1Il
    if lll11llI == IlllII11:
        if not I1IIIIII:
            lll11llI = llI1llll
        else:
            lll11llI = Il1I11II
    if lll11llI == llI1llll:
        l1l1Illl = I11l1IIl
    if lll11llI == Il111lll:
        l1l1Illl = llII11lI
    if l1l1Illl == llII11lI:
        I1II1111 = Il1lIlI1
        if not IIllI111:
            I1II1111 = II11l1Il
        else:
            I1II1111 = llI11111
        if I1II1111 == llI11111:
            if not IIIIIIll:
                I1II1111 = I1l11l11
            else:
                I1II1111 = II11l1Il
        if I1II1111 == I1l11l11:
            l1l1Illl = I11l1IIl
        if I1II1111 == llllIlIl:
            l1l1Illl = l11llI11
    if l1l1Illl == lI1II1l1:
        Ill1Il1l = Ill1Il1l[l1Ill1lI:]
    if l1l1Illl == Il111lll:
        pass
    lIII1I1l = QueuedEvent(I1IIl1l1, Ill1Il1l, I1I1llll)
    with lockguard.LockGuard(l1l11llI._queueListLock):
        l1l11llI._queueList.append(lIII1I1l)
    I11I1l1l = l1llI1II
    l1Il11II = llllII1I
    if not lIIIIII1:
        l1Il11II = ll1I1IlI
    else:
        l1Il11II = l1III1II
    if l1Il11II == lll111l1:
        if I1Il1lIl(llI11III, I1l1Il11):
            l1Il11II = Il111lll
        else:
            l1Il11II = llI1llll
    if l1Il11II == lIII111l:
        I11I1l1l = lIIIIII1
    if l1Il11II == llI1llll:
        I11I1l1l = Ill1I1lI
    if I11I1l1l == II1l1llI:
        I1IllllI = I1IIIIII
        if not l1l11llI._doCanProcess():
            I1IllllI = lll11lI1
        else:
            I1IllllI = l1l1I1lI
        if I1IllllI == lll11lI1:
            if IIll1I1I(ll1IlIll, llII11lI):
                I1IllllI = lIIIl1l1
            else:
                I1IllllI = l1llI1II
        if I1IllllI == I1I11l11:
            I11I1l1l = Ill1I1lI
        if I1IllllI == lIIIl1l1:
            I11I1l1l = llIII11l
    if I11I1l1l == ll1l1I11:
        with lockguard.LockGuard(l1l11llI._queueListMutex):
            l1l11llI._queueListConditionVariable.notify()
    if I11I1l1l == I11l1IIl:
        pass

def IIIlll11(ll1IIlI1):
    return not (ll1IIlI1._queueList or I1Il1lIl(ll1IIlI1._queueEmptyCounter, lI1IllI1))

def I1llll1l(I111IlI1):
    with lockguard.LockGuard(I111IlI1._queueListLock):
        I111IlI1._queueList = []

def I1111lII(ll1lIlII):
    I1l11III = I11111l1
    IlI1II11 = Il1l111l
    if not ll1lIlII._queueList:
        IlI1II11 = I1l1lIlI
    else:
        IlI1II11 = Ill1I1lI
    if IlI1II11 == ll1l1I11:
        if not I111I1Il(IIlll11I):
            IlI1II11 = l111ll1l
        else:
            IlI1II11 = lIl1l1I1
    if IlI1II11 == lIl1l1I1:
        I1l11III = I1I11l11
    if IlI1II11 == lIII1lI1:
        I1l11III = I1lIIlll
    if I1l11III == I1lIIlll:
        II11I1ll = I1l1lIIl
        if not IIlIIIIl.I111lIl1(lIlllI11):
            II11I1ll = IIlllIII
        else:
            II11I1ll = l1l1I1lI
        if II11I1ll == l1l1I1lI:
            if I1IllIll(IIllllIl, Il1lllII):
                II11I1ll = I1l1lIlI
            else:
                II11I1ll = IIlllIII
        if II11I1ll == IIIll111:
            I1l11III = II1IIl1l
        if II11I1ll == lllIII1I:
            I1l11III = ll1IllII
    if I1l11III == l1llI1II:
        with lockguard.LockGuard(ll1lIlII._queueListLock):
            Il111lIl = ll1lIlII._queueList
            ll1lIlII._queueList = []
        ll1II1Il = II1II1I1
        lII1l1lI = I1I1I1Il
        if not ll1lI1lI(lI1llll1):
            lII1l1lI = IlI11lIl
        else:
            lII1l1lI = I1IIIIII
        if lII1l1lI == l1II11Il:
            if IIll1I1I(llII11II, lIlI1I11):
                lII1l1lI = I1IIIIII
            else:
                lII1l1lI = l11I1III
        if lII1l1lI == I11111l1:
            ll1II1Il = IIllI111
        if lII1l1lI == Il11Illl:
            ll1II1Il = IllIII11
        if ll1II1Il == I1l11l11:
            I1lIllI1 = II11l1Il
            if not Il111lIl:
                I1lIllI1 = IIllll11
            else:
                I1lIllI1 = lIIllIlI
            if I1lIllI1 == lIIlll1l:
                if not I111I1Il(IIl1II11):
                    I1lIllI1 = l111I111
                else:
                    I1lIllI1 = llllI1Il
            if I1lIllI1 == Il1I1llI:
                ll1II1Il = lI11lllI
            if I1lIllI1 == Ill11l11:
                ll1II1Il = I1IlI1Il
        if ll1II1Il == II1ll1ll:
            while (I111I1Il(I1IlIIIl) and lI11l11l) and (llIIl11I > ll11II11 and Ill1lI11) or ((Il1I1llI != Il1I1llI and l1Ill1lI) and (ll1lI1lI(I1llI1I1) and llIIIlll)):
                while ((not I111I1Il(lII11lIl) or not I1I11Il1) or (not l11l11ll and I111I1Il(I111I1II))) or (not ll1lI1lI(lIlI1l1l) and I1l1111l or (I111I1Il(I1llI1II) and l1IIl111 == l1IIl111)):
                    while ((not IIlIIIIl.I111lIl1(lI11II1I) or not IIlIIIIl.I111lIl1(I1IIlIlI)) or (l1Ill11l == l1Ill11l or not IIIllIlI)) and ((IIl1I1I1 and I1l1ll11 != IIl111l1) and (I111I1Il(Ill1I1lI) and IIlIIIIl.I111lIl1(l1l1I1lI))):
                        for lIl11Il1 in Il111lIl:
                            IIl11II1 = I1IIIIII
                            I11llIll = l11I1III
                            if not lII1I11l:
                                I11llIll = l1Ill11l
                            else:
                                I11llIll = l11I1IIl
                            if I11llIll == l111IIIl:
                                if not I111I1Il(lIlllI11):
                                    I11llIll = ll1IlIll
                                else:
                                    I11llIll = I1l11l11
                            if I11llIll == I1lIllll:
                                IIl11II1 = l111I11l
                            if I11llIll == l1IIl111:
                                IIl11II1 = ll1Illl1
                            if IIl11II1 == ll1Illl1:
                                lIlllI1I = Il1l1l1I
                                if not I111I1Il(I1IIlIlI):
                                    lIlllI1I = lI11llI1
                                else:
                                    lIlllI1I = Ill1lIIl
                                if lIlllI1I == IIIllIlI:
                                    IllllIlI = llllII1I
                                    l1II1I1l = IIllI111
                                    l1I1I1I1 = lII1I11l
                                    if not IIlIIIIl.I111lIl1(Il11l1II):
                                        l1I1I1I1 = lIlIlll1
                                    else:
                                        l1I1I1I1 = lII1IIll
                                    if l1I1I1I1 == l11llI11:
                                        if not I111I1Il(I1l11l11):
                                            l1I1I1I1 = ll1lll11
                                        else:
                                            l1I1I1I1 = l11I1III
                                    if l1I1I1I1 == l11I1III:
                                        l1II1I1l = llIIIlll
                                    if l1I1I1I1 == lIlIlll1:
                                        l1II1I1l = I1IIIIII
                                    if l1II1I1l == llIIIlll:
                                        Illlll1l = Illll1lI
                                        if IIll1I1I(lII1llIl, Illll1lI):
                                            Illlll1l = lIlllI11
                                        else:
                                            Illlll1l = lIIlll1l
                                        if Illlll1l == lIIllIlI:
                                            if Il1lI1Il(lIlIlll1, II1ll1Il):
                                                Illlll1l = lIlllI11
                                            else:
                                                Illlll1l = IlI1lI11
                                        if Illlll1l == IIl1I1I1:
                                            l1II1I1l = l1III1Il
                                        if Illlll1l == lIlI1l1l:
                                            l1II1I1l = I1IIIIII
                                    if l1II1I1l == I1IIIIII:
                                        IllllIlI = l11l11ll
                                    if l1II1I1l == IIIl1IIl:
                                        IllllIlI = lll111l1
                                    if IllllIlI == l1III1II:
                                        l1IIII1I = IlllIl1I
                                        lIl111lI = II11l1Il
                                        if not I1lIlIIl:
                                            lIl111lI = I1lIII1I
                                        else:
                                            lIl111lI = l11I1III
                                        if lIl111lI == l11I1III:
                                            if not IIlIIIIl.I111lIl1(I1llI1II):
                                                lIl111lI = IlI11lIl
                                            else:
                                                lIl111lI = I1I11I1l
                                        if lIl111lI == l11I111I:
                                            l1IIII1I = IIIIIllI
                                        if lIl111lI == IlI11lIl:
                                            l1IIII1I = lll1ll1l
                                        if l1IIII1I == I11lIlII:
                                            lIIl1II1 = I11l1IIl
                                            if llII1l1I(I1lII11l, lll1IIl1):
                                                lIIl1II1 = l1I1Ill1
                                            else:
                                                lIIl1II1 = llI1llll
                                            if lIIl1II1 == I1lII11l:
                                                if not I111I1Il(IIl1II11):
                                                    lIIl1II1 = l1lIll11
                                                else:
                                                    lIIl1II1 = lII11lIl
                                            if lIIl1II1 == I1I11Il1:
                                                l1IIII1I = lI1llll1
                                            if lIIl1II1 == l1I1Ill1:
                                                l1IIII1I = l1llII11
                                        if l1IIII1I == IIllll11:
                                            IllllIlI = l11ll1Il
                                        if l1IIII1I == IlI1I1ll:
                                            IllllIlI = IIIII111
                                    if IllllIlI == IIIII111:
                                        lIlllI1I = lIl1l1I1
                                    if IllllIlI == IIlllIlI:
                                        lIlllI1I = I1l1Il11
                                if lIlllI1I == lll1ll1l:
                                    IIl11II1 = lIl1l1I1
                                if lIlllI1I == I1l1Il11:
                                    IIl11II1 = IIlI1III
                            if IIl11II1 == lI1llll1:
                                ll1lIlII.directDispatch(lIl11Il1.event, *lIl11Il1.args, **lIl11Il1.kwargs)
                            if IIl11II1 == Ill1lIIl:
                                pass
                        break
                    break
                break
            return lll1I1I1
        if ll1II1Il == IlllIlIl:
            pass
    if I1l11III == II1I1I1I:
        pass
    return I11llIl1

def llI1IIll(lIIll1I1):
    ll1111I1 = I1ll11lI
    ll1llII1 = l1IIl111
    if not ll1lI1lI(l111ll1l):
        ll1llII1 = llI11111
    else:
        ll1llII1 = IIlIl11I
    if ll1llII1 == IIII1I1I:
        if not ll1lI1lI(llIII1II):
            ll1llII1 = llI11111
        else:
            ll1llII1 = I1llI1II
    if ll1llII1 == I1I11I1l:
        ll1111I1 = Ill11IlI
    if ll1llII1 == Il111IIl:
        ll1111I1 = I1Ill11l
    if ll1111I1 == l11II1I1:
        II11IIII = I1IIlIIl
        if not ll1lI1lI(I1I1IIIl):
            II11IIII = IIlll11I
        else:
            II11IIII = lIlllI11
        if II11IIII == lIlllI11:
            if not lIIll1I1._queueList:
                II11IIII = IlllIlIl
            else:
                II11IIII = lII11lIl
        if II11IIII == lII11lIl:
            ll1111I1 = I1l1111l
        if II11IIII == IlllIl1l:
            ll1111I1 = lIIIl1l1
    if ll1111I1 == l1III1II:
        lII1lIII = lIl11lIl
        with lockguard.LockGuard(lIIll1I1._queueListLock):
            l11lIl1I = IIIlllll
            IIIlIlIl = ll111llI
            if I1IllIll(III1I1I1, lIlIlll1):
                IIIlIlIl = lIlIlll1
            else:
                IIIlIlIl = IIlll11I
            if IIIlIlIl == IIlll11I:
                if not ll1lI1lI(lI1111lI):
                    IIIlIlIl = ll1lll11
                else:
                    IIIlIlIl = I1lII11l
            if IIIlIlIl == I1lII11l:
                l11lIl1I = lII1I11l
            if IIIlIlIl == l11l11II:
                l11lIl1I = llllII1I
            if l11lIl1I == l111I1Il:
                llIlI1I1 = Il11IlI1
                if not lIIll1I1._queueList:
                    llIlI1I1 = lI1II1l1
                else:
                    llIlI1I1 = IIIllIlI
                if llIlI1I1 == lIl11I1I:
                    if not l11l11ll:
                        llIlI1I1 = IIII1l11
                    else:
                        llIlI1I1 = IIIll1II
                if llIlI1I1 == ll11lIll:
                    l11lIl1I = lIlllI11
                if llIlI1I1 == IIIl1I1l:
                    l11lIl1I = IIII1I1I
            if l11lIl1I == llllII1I:
                pass
            if l11lIl1I == IIl1II11:
                lII1lIII = lIIll1I1._queueList[IIllIlII]
                lIIll1I1._queueList = lIIll1I1._queueList[IlI111I1:]
        lIIIl11l = l1llI1II
        lll1I1II = I1I1111I
        if not I111I1Il(lllIII1I):
            lll1I1II = I1llIllI
        else:
            lll1I1II = IIllllIl
        if lll1I1II == Illl1l11:
            if not l1llI1II:
                lll1I1II = ll1lII1I
            else:
                lll1I1II = Ill1111I
        if lll1I1II == ll1lII1I:
            lIIIl11l = l1III1II
        if lll1I1II == l1lIll11:
            lIIIl11l = II1I1IIl
        if lIIIl11l == II1I1IIl:
            lII1I1II = llIII11l
            if not ll1lI1lI(I1l11l11):
                lII1I1II = lIlII1l1
            else:
                lII1I1II = I1IlIIIl
            if lII1I1II == IlllII11:
                if lII1lIII is IlI1IIll:
                    lII1I1II = I1I1111I
                else:
                    lII1I1II = lIlIlll1
            if lII1I1II == l11l11II:
                lIIIl11l = I1Ill11l
            if lII1I1II == I1I1111I:
                lIIIl11l = llI1llll
        if lIIIl11l == I1l1111l:
            lIIll1I1.directDispatch(lII1lIII.event, *lII1lIII.args, **lII1lIII.kwargs)
            return I1l1IIl1
        if lIIIl11l == I1lII11l:
            pass
    if ll1111I1 == IlllI1II:
        pass
    return I11llIl1

def lll1IIII(lI111lI1, IIlI1I1I):
    lll1llI1 = I11IIlIl
    IlIIIl11 = IlII1ll1
    if not ll1l11II:
        IlIIIl11 = l1I1Ill1
    else:
        IlIIIl11 = Illl1l11
    if IlIIIl11 == lI1IIlII:
        if not ll1lI1lI(l1I1IIIl):
            IlIIIl11 = Ill1111I
        else:
            IlIIIl11 = lIIlll1l
    if IlIIIl11 == lIIllIlI:
        lll1llI1 = Ill1l1lI
    if IlIIIl11 == l1lI1I1l:
        lll1llI1 = Ill11IlI
    if lll1llI1 == Ill1l1lI:
        III1llI1 = l11I1l11
        if not lI111lI1._queueList:
            III1llI1 = III111lI
        else:
            III1llI1 = l1I111ll
        if III1llI1 == lIIlI11I:
            if not ll1lI1lI(l1I1IIIl):
                III1llI1 = l1I1IIIl
            else:
                III1llI1 = I1IlIIIl
        if III1llI1 == IlI1llII:
            lll1llI1 = I1l1IlI1
        if III1llI1 == lll1IIlI:
            lll1llI1 = lIII111l
    if lll1llI1 == Ill11IlI:
        pass
    if lll1llI1 == Il1I11II:
        with lockguard.LockGuard(lI111lI1._queueListLock):
            ll1I1I1l = lI111lI1._queueList
            lI111lI1._queueList = []
        I1II1Il1 = llI11Ill
        lIlIlI11 = l1l1Il11
        if not IIlIIIIl.I111lIl1(IIIIIIll):
            lIlIlI11 = I111111l
        else:
            lIlIlI11 = I1I1111I
        if lIlIlI11 == lII11111:
            if not I111I1Il(IIII1I1I):
                lIlIlI11 = IIIll1II
            else:
                lIlIlI11 = IlI1llII
        if lIlIlI11 == Ill11l11:
            I1II1Il1 = IlIIIl1I
        if lIlIlI11 == I111111l:
            I1II1Il1 = Il1lIlI1
        if I1II1Il1 == Il1111Il:
            I1IIl111 = IIII1I1I
            if not I111I1Il(I11llIl1):
                I1IIl111 = Il1l1l1I
            else:
                I1IIl111 = I1l1Il11
            if I1IIl111 == Il1I1l1I:
                if not ll1I1I1l:
                    I1IIl111 = lIIlll1l
                else:
                    I1IIl111 = IlIIII11
            if I1IIl111 == llI11Ill:
                I1II1Il1 = lIlIIl1I
            if I1IIl111 == lIIlll1l:
                I1II1Il1 = Il1lIlI1
        if I1II1Il1 == lIl11I1I:
            pass
        if I1II1Il1 == I1IIlIlI:
            for IllIllIl in ll1I1I1l:
                lIlIlIII = l1Ill11l
                lIIll111 = I1l1lIII
                if not ll1lI1lI(lIIlII11):
                    lIIll111 = l1IIl111
                else:
                    lIIll111 = lIlllI11
                if lIIll111 == llIl11ll:
                    if llII1l1I(llIlIlI1, IlI11lIl):
                        lIIll111 = II1I1ll1
                    else:
                        lIIll111 = IllIII11
                if lIIll111 == I1l11l11:
                    lIlIlIII = l1Ill1lI
                if lIIll111 == II1I1ll1:
                    lIlIlIII = lIIIIll1
                if lIlIlIII == l111llll:
                    IIll11Il = I111111l
                    if not IIlIIIIl.I111lIl1(l1I1IIIl):
                        IIll11Il = I11IIlI1
                    else:
                        IIll11Il = I1llIllI
                    if IIll11Il == l1I1Ill1:
                        l11lIl1l = ll1lI1I1
                        Ill1I11l = II1l1ll1
                        ll111I1l = lll1IIlI
                        if not ll1lI1lI(ll1l1I11):
                            ll111I1l = I1I1111I
                        else:
                            ll111I1l = lIlI1I11
                        if ll111I1l == lIlI1I11:
                            if not IIlIIIIl.I111lIl1(Il11Illl):
                                ll111I1l = I1I1111I
                            else:
                                ll111I1l = I1ll11lI
                        if ll111I1l == l1IlIl1I:
                            Ill1I11l = Il111IIl
                        if ll111I1l == I1ll11lI:
                            Ill1I11l = I1I1III1
                        if Ill1I11l == l1IIll11:
                            I1lI11ll = II11l1Il
                            if lIlI11ll(lIlII1ll, Il1l1l1I):
                                I1lI11ll = I11111l1
                            else:
                                I1lI11ll = I1l1111l
                            if I1lI11ll == Il1l111l:
                                if I1Il1lIl(IlllIlII, I1Ill11l):
                                    I1lI11ll = llI11111
                                else:
                                    I1lI11ll = lll111l1
                            if I1lI11ll == lIllI111:
                                Ill1I11l = IlI1lI11
                            if I1lI11ll == IIlllIII:
                                Ill1I11l = lII1I11l
                        if Ill1I11l == I11IIl1l:
                            l11lIl1l = l11ll11I
                        if Ill1I11l == IlI1lI11:
                            l11lIl1l = I11II11l
                        if l11lIl1l == l11ll11I:
                            I11l11II = llIII1II
                            l11111Il = Il11I1ll
                            if lIlI11ll(IlI1I1ll, IlIllllI):
                                l11111Il = l1lI1l1I
                            else:
                                l11111Il = IIII1III
                            if l11111Il == l1lI1l1I:
                                if not I111I1Il(I1llI1Il):
                                    l11111Il = IIlllI1l
                                else:
                                    l11111Il = IlIIIl1I
                            if l11111Il == IIlllI1l:
                                I11l11II = l111l11I
                            if l11111Il == IIl11ll1:
                                I11l11II = lI1IIlII
                            if I11l11II == I11I11ll:
                                I1I1IlII = ll1l11II
                                if not l111llll:
                                    I1I1IlII = lIII1lI1
                                else:
                                    I1I1IlII = lI11l11l
                                if I1I1IlII == IlIIIIlI:
                                    if not lIlI1lll:
                                        I1I1IlII = l1llllII
                                    else:
                                        I1I1IlII = l111ll1l
                                if I1I1IlII == I1l1lIlI:
                                    I11l11II = l11IlI1I
                                if I1I1IlII == IlIIIl1I:
                                    I11l11II = Il1lllII
                            if I11l11II == IIllIllI:
                                l11lIl1l = lIIllIlI
                            if I11l11II == Il1lllII:
                                l11lIl1l = lIllI111
                        if l11lIl1l == I1Ill11l:
                            IIll11Il = lI1I1l1l
                        if l11lIl1l == lIIllIlI:
                            IIll11Il = I1lllll1
                    if IIll11Il == I1I11l11:
                        lIlIlIII = l1Ill1lI
                    if IIll11Il == lI1I1l1l:
                        lIlIlIII = I11lIlII
                if lIlIlIII == I1llI1I1:
                    pass
                if lIlIlIII == I1lIllIl:
                    IllI1Il1 = Il1l111l
                    IIl1lll1 = II11l1Il
                    if not IIlIIIIl.I111lIl1(I1IIlIlI):
                        IIl1lll1 = lIIllll1
                    else:
                        IIl1lll1 = lI1I1l1l
                    if IIl1lll1 == l111I1Il:
                        if not I111I1Il(Il1l11l1):
                            IIl1lll1 = llIII1II
                        else:
                            IIl1lll1 = I1l1ll11
                    if IIl1lll1 == lIIIl1l1:
                        IllI1Il1 = lI11lllI
                    if IIl1lll1 == lIIllll1:
                        IllI1Il1 = l1III1II
                    if IllI1Il1 == ll11II11:
                        I11IllIl = lI11llI1
                        if not IIlI1I1I(*IllIllIl.args, **IllIllIl.kwargs):
                            I11IllIl = I11IIlIl
                        else:
                            I11IllIl = IIlI1III
                        if I11IllIl == IIIllIlI:
                            if not I1Ill11l:
                                I11IllIl = IlIlI1ll
                            else:
                                I11IllIl = I11I11ll
                        if I11IllIl == lI1IIlII:
                            IllI1Il1 = I1Ill11l
                        if I11IllIl == l111l11I:
                            IllI1Il1 = Il1I1llI
                    if IllI1Il1 == lIllI111:
                        lI111lI1._queueList.append(IllIllIl)
                    if IllI1Il1 == l111I111:
                        lI111lI1.directDispatch(IllIllIl.event, *IllIllIl.args, **IllIllIl.kwargs)
            return I1l1IIl1
    return I11llIl1

def l1l11l1I(lII1II11):
    with lockguard.LockGuard(lII1II11._queueListMutex):
        for I1IlIIl1 in [lIlI1I11]:
            while IIlll1lI:
                IlIIlI1l = II11l1Il
                IIl1IIll = I11lIlII
                if I1IllIll(llllllll, llllllll):
                    IIl1IIll = IlllIl1I
                else:
                    IIl1IIll = lll11I1I
                if IIl1IIll == IlIlIIII:
                    if lIlI11ll(l11I1IIl, l1I1IIIl):
                        IIl1IIll = I1IIII1l
                    else:
                        IIl1IIll = II11IlI1
                if IIl1IIll == l11I1IIl:
                    IlIIlI1l = lIIlIl11
                if IIl1IIll == IIlI1ll1:
                    IlIIlI1l = llII11lI
                if IlIIlI1l == lIlI1I11:
                    IlIlI11l = l1lI1I1l
                    if Il1lI1Il(l111IIIl, Ill1l1lI):
                        IlIlI11l = l11llI11
                    else:
                        IlIlI11l = lllI1I1l
                    if IlIlI11l == lIl11I1I:
                        l1ll1I11 = IIIIIllI
                        IIllI1l1 = llIlI11l
                        l1II1IlI = lIIlIl11
                        if not I111I1Il(II1ll1ll):
                            l1II1IlI = I1IIlIlI
                        else:
                            l1II1IlI = l1IIll11
                        if l1II1IlI == IIlllIII:
                            if not IIlIIIIl.I111lIl1(I1lII11l):
                                l1II1IlI = IIll1I1l
                            else:
                                l1II1IlI = Il1I11II
                        if l1II1IlI == lIlIIl1I:
                            IIllI1l1 = llllII1I
                        if l1II1IlI == Il111lll:
                            IIllI1l1 = llIIIlll
                        if IIllI1l1 == lI1ll1l1:
                            III1Ill1 = l1lIlllI
                            if I1IllIll(l11I1l11, lIlII1ll):
                                III1Ill1 = I1I11Il1
                            else:
                                III1Ill1 = I1IlI1Il
                            if III1Ill1 == IIlll11I:
                                if not I111I1Il(IllI1lI1):
                                    III1Ill1 = I1IlI1Il
                                else:
                                    III1Ill1 = llI11III
                            if III1Ill1 == I1IlI1Il:
                                IIllI1l1 = lIlllI11
                            if III1Ill1 == l11llI11:
                                IIllI1l1 = l11I1IIl
                        if IIllI1l1 == lll11I1I:
                            l1ll1I11 = Il11IlI1
                        if IIllI1l1 == lIlllI11:
                            l1ll1I11 = llllIlIl
                        if l1ll1I11 == ll111llI:
                            II1lIIll = IllI1lI1
                            I1IIII11 = l1I1I11l
                            if not IIlIIIIl.I111lIl1(lll11I1I):
                                I1IIII11 = lIllI111
                            else:
                                I1IIII11 = I1IIlIlI
                            if I1IIII11 == IlIIIIlI:
                                if not IIlIIIIl.I111lIl1(l1III1Il):
                                    I1IIII11 = l1III1II
                                else:
                                    I1IIII11 = I1llI1I1
                            if I1IIII11 == lIllI111:
                                II1lIIll = Ill11l11
                            if I1IIII11 == IIIIIllI:
                                II1lIIll = IIllI111
                            if II1lIIll == IlI1llII:
                                lIII1l1I = ll1lII1I
                                if not IIIll1II:
                                    lIII1l1I = Il111lll
                                else:
                                    lIII1l1I = III11l11
                                if lIII1l1I == llII11lI:
                                    if not I111I1Il(l1IIllI1):
                                        lIII1l1I = l1I1111l
                                    else:
                                        lIII1l1I = Il1I11II
                                if lIII1l1I == l1I1111l:
                                    II1lIIll = l11ll11I
                                if lIII1l1I == lIII111l:
                                    II1lIIll = IlII11I1
                            if II1lIIll == Il11I1ll:
                                l1ll1I11 = IIlllI1l
                            if II1lIIll == IlII11I1:
                                l1ll1I11 = IIIl1IIl
                        if l1ll1I11 == IIIl1IIl:
                            IlIlI11l = I11I11ll
                        if l1ll1I11 == I1IIII1l:
                            IlIlI11l = Ill1l1lI
                    if IlIlI11l == ll1I1lll:
                        IlIIlI1l = Il11Illl
                    if IlIlI11l == IllI11Il:
                        IlIIlI1l = I1lIllII
                if IlIIlI1l == IIIIIllI:
                    pass
                if IlIIlI1l == I1IIIIII:
                    lII1II11._queueListConditionVariable.wait(Il1lIl1I)
                    IIl1lI1l = I11II11l
                    lIIl1lII = lllI1I1l
                    if not I111I1Il(llIl11ll):
                        lIIl1lII = lllIII1I
                    else:
                        lIIl1lII = ll11II11
                    if lIIl1lII == lI11lllI:
                        if not IllIII11:
                            lIIl1lII = II11l1Il
                        else:
                            lIIl1lII = lIII1lI1
                    if lIIl1lII == IIlllI1l:
                        IIl1lI1l = l11ll11I
                    if lIIl1lII == III11I1I:
                        IIl1lI1l = lIlIl11I
                    if IIl1lI1l == IllIII11:
                        lllIl11I = Illl1l11
                        if not lII1II11._doCanProcess():
                            lllIl11I = l1llII11
                        else:
                            lllIl11I = IlIIIIlI
                        if lllIl11I == IIllll11:
                            if not I1IllIll(l1IIl111, I1l11l11):
                                lllIl11I = IlIIIIlI
                            else:
                                lllIl11I = II1I1I1I
                        if lllIl11I == l1II11Il:
                            IIl1lI1l = ll11II11
                        if lllIl11I == I1I1I1Il:
                            IIl1lI1l = I1IlI1Il
                    if IIl1lI1l == IIIIIIll:
                        break
                    if IIl1lI1l == ll1l11II:
                        pass

def l11lIII1(I1lIIl1l, II1l1lI1):
    with lockguard.LockGuard(I1lIIl1l._queueListMutex):
        I1I11I11 = time.time()
        while lll1I1I1:
            l1I1l11l = I1lIIlll
            lll1IlI1 = IIIl1IIl
            if not I111I1Il(I1l1lIII):
                lll1IlI1 = llII11lI
            else:
                lll1IlI1 = I11I11ll
            if lll1IlI1 == l111l11I:
                if not lIlllI11:
                    lll1IlI1 = lIll1I1I
                else:
                    lll1IlI1 = I1lIllII
            if lll1IlI1 == I11lI1l1:
                l1I1l11l = l111I111
            if lll1IlI1 == IIIIIllI:
                l1I1l11l = l1Il1Ill
            if l1I1l11l == lll11I1I:
                lIllll11 = IlI11lIl
                I1Il1IIl = lIlIIl1I
                l111l1lI = lI1ll1l1
                lIIll11l = Illl1l11
                if llII1l1I(II11l1Il, l111I1Il):
                    lIIll11l = I1IIII1l
                else:
                    lIIll11l = l1III1Il
                if lIIll11l == lIl1IlI1:
                    if llII1l1I(l1III111, lIl1IIl1):
                        lIIll11l = IIII1III
                    else:
                        lIIll11l = I111l1I1
                if lIIll11l == I111l1I1:
                    l111l1lI = IlI11lIl
                if lIIll11l == II11l1Il:
                    l111l1lI = lIlIlll1
                if l111l1lI == l11l11II:
                    lIIl11l1 = l1lI1I1l
                    if not ll1lI1lI(l11I111I):
                        lIIl11l1 = llIl11ll
                    else:
                        lIIl11l1 = II1l1llI
                    if lIIl11l1 == II1l1llI:
                        if Il1lI1Il(I1l1lII1, Il11IlI1):
                            lIIl11l1 = III1ll11
                        else:
                            lIIl11l1 = I1lIllII
                    if lIIl11l1 == I1lIllII:
                        l111l1lI = II1I1I1I
                    if lIIl11l1 == llIl11ll:
                        l111l1lI = IIlll11I
                if l111l1lI == IlllIl1I:
                    I1Il1IIl = lIIlll1l
                if l111l1lI == IlI11lIl:
                    I1Il1IIl = IlIIlll1
                if I1Il1IIl == lIl1IlI1:
                    l1I1III1 = lIIlll1l
                    ll111ll1 = IllIl1Il
                    if not IIlIIIIl.I111lIl1(lI1I1l1I):
                        ll111ll1 = IIl1II11
                    else:
                        ll111ll1 = IIIII111
                    if ll111ll1 == lI1111lI:
                        if IIll1I1I(Il11IIlI, I1IIII1l):
                            ll111ll1 = I11lIlII
                        else:
                            ll111ll1 = lIIIIll1
                    if ll111ll1 == I1llI1Il:
                        l1I1III1 = l1Ill1lI
                    if ll111ll1 == llII11lI:
                        l1I1III1 = II1I1ll1
                    if l1I1III1 == l1Ill1lI:
                        IIII111I = I1l111l1
                        if not IIlIIIIl.I111lIl1(ll111llI):
                            IIII111I = Ill1lI11
                        else:
                            IIII111I = lII1llIl
                        if IIII111I == IlllIl1l:
                            if I1IllIll(lIII1lI1, I1IlI11l):
                                IIII111I = IIIl1IIl
                            else:
                                IIII111I = II1ll1Il
                        if IIII111I == IlIIlll1:
                            l1I1III1 = I1IIIIII
                        if IIII111I == IIIllIll:
                            l1I1III1 = llIl1Ill
                    if l1I1III1 == Il11Illl:
                        I1Il1IIl = I11II11l
                    if l1I1III1 == llllI1Il:
                        I1Il1IIl = lllI1I1l
                if I1Il1IIl == lllI1I1l:
                    lIllll11 = IlI1llII
                if I1Il1IIl == lIIlll1l:
                    lIllll11 = II1l1llI
                if lIllll11 == lIIIIII1:
                    if not I111I1Il(I11IlIII):
                        lIllll11 = IlllII11
                    else:
                        lIllll11 = IlIlIIII
                if lIllll11 == I1I11Il1:
                    l1I1l11l = IlllIl1I
                if lIllll11 == IlI1llII:
                    l1I1l11l = IIllll11
            if l1I1l11l == lII11lIl:
                pass
            if l1I1l11l == Il1I1llI:
                I1lIIl1l._queueListConditionVariable.wait(Il1lIl1I)
                IIl1lIII = l1IIl111
                lllll1Il = I1l1lIlI
                if not ll1l1I11:
                    lllll1Il = lllll1ll
                else:
                    lllll1Il = lIl11I1I
                if lllll1Il == l11llI11:
                    if Il1lI1Il(l1I1Ill1, I111I1lI):
                        lllll1Il = l111IIIl
                    else:
                        lllll1Il = lllll1ll
                if lllll1Il == lIIlI11I:
                    IIl1lIII = l111llll
                if lllll1Il == l111IIIl:
                    IIl1lIII = I1I1IIIl
                if IIl1lIII == llll1lI1:
                    l1IlIlll = IIIlII1l
                    if not I1lIIl1l._doCanProcess():
                        l1IlIlll = lI1I1l1I
                    else:
                        l1IlIlll = Il1I1llI
                    if l1IlIlll == lI1I1l1I:
                        if not I111I1Il(l111IIIl):
                            l1IlIlll = lIl1l1ll
                        else:
                            l1IlIlll = l1III1II
                    if l1IlIlll == l1III1II:
                        IIl1lIII = I1I11Il1
                    if l1IlIlll == l111I111:
                        IIl1lIII = IIlIl11I
                if IIl1lIII == IlIlIIII:
                    pass
                if IIl1lIII == I1llI1Il:
                    return I1ll1I1I
                I1111l11 = l11l11II
                Il1II1ll = ll1l11II
                if not I1IllIll(ll1lll11, Illl1llI):
                    Il1II1ll = ll1IIll1
                else:
                    Il1II1ll = I11l1IIl
                if Il1II1ll == Il1I11II:
                    if not I11IIl1l:
                        Il1II1ll = I1lIllIl
                    else:
                        Il1II1ll = IIllllIl
                if Il1II1ll == III1IIll:
                    I1111l11 = I1l11l11
                if Il1II1ll == I11IIlIl:
                    I1111l11 = I11IIl1l
                if I1111l11 == lIII11l1:
                    IlI1I1Il = III111Il
                    if not IIll1I1I(time.time() - I1I11I11, II1l1lI1):
                        IlI1I1Il = llll1lI1
                    else:
                        IlI1I1Il = lllIII1I
                    if IlI1I1Il == lIlIlll1:
                        if not IIlIIIIl.I111lIl1(Il1lIlI1):
                            IlI1I1Il = llIlI11l
                        else:
                            IlI1I1Il = l11lII1l
                    if IlI1I1Il == l11lII1l:
                        I1111l11 = IIl11I11
                    if IlI1I1Il == l111ll1l:
                        I1111l11 = II1I1ll1
                if I1111l11 == II1I1ll1:
                    pass
                if I1111l11 == l1IIl111:
                    return l1I11Ill

def II11Il1l(I1IIIlII, I1ll111I):
    I1ll111I.directDispatch(I1IIIlII.event, *I1IIIlII.args, **I1IIIlII.kwargs)

def I1llIlll(l1I1l1Il):
    l1II11I1 = lIIlII11
    II1l1111 = lII1llIl
    if not l1I1l1Il._queueList:
        II1l1111 = Il1lIlIl
    else:
        II1l1111 = I1lIllll
    if II1l1111 == Il1l1l1I:
        if not llII1l1I(I1I1IIIl, III11l11):
            II1l1111 = Il1I1llI
        else:
            II1l1111 = I1I1111I
    if II1l1111 == l111I111:
        l1II11I1 = lI1111lI
    if II1l1111 == lII11111:
        l1II11I1 = I1IIlIIl
    if l1II11I1 == lI1111lI:
        II1111ll = l1llI1II
        if not I111I1Il(ll1lII1I):
            II1111ll = I1I11Il1
        else:
            II1111ll = lI1I1l1I
        if II1111ll == I1lIllIl:
            if not lIlI11ll(Ill1I1lI, lI11l1I1):
                II1111ll = lIllI111
            else:
                II1111ll = IIlll11I
        if II1111ll == lIllI111:
            l1II11I1 = l11llI11
        if II1111ll == IlIlIIII:
            l1II11I1 = lIIIIII1
    if l1II11I1 == l11llI11:
        with lockguard.LockGuard(l1I1l1Il._queueListLock):
            lllllIIl = ll1IIllI
            IlIII1I1 = Il1lIlI1
            if not I111I1Il(I11llIl1):
                IlIII1I1 = Illl1l11
            else:
                IlIII1I1 = l11I111I
            if IlIII1I1 == IlIlI1ll:
                if not I111I1Il(lllI1I1l):
                    IlIII1I1 = I1llI1II
                else:
                    IlIII1I1 = I1I1III1
            if IlIII1I1 == I1I11I1l:
                lllllIIl = lIIIIll1
            if IlIII1I1 == I11IIl1l:
                lllllIIl = l1l1Il11
            if lllllIIl == IIII1I1I:
                l111l111 = lIlIlll1
                if not IIlIIIIl.I111lIl1(IIllll11):
                    l111l111 = l111ll1l
                else:
                    l111l111 = IIl1I1I1
                if l111l111 == lIlllI11:
                    if not l1I1l1Il._queueList:
                        l111l111 = I1l1lIlI
                    else:
                        l111l111 = l1lI1I1l
                if l111l111 == lllIII1I:
                    lllllIIl = Illl1l11
                if l111l111 == l1lIll11:
                    lllllIIl = lI11I1II
            if lllllIIl == lI1IIlII:
                pass
            if lllllIIl == Il11Illl:
                return l1I1l1Il._queueList[IIllIlII]
    if l1II11I1 == II1l1llI:
        pass
    return IlI1IIll

def l1l11Ill(I111I1ll):
    Illll1Il = Il111lI1
    l1lII1ll = Il1I11II
    if not IIll1I1I(I1I1III1, III1I1I1):
        l1lII1ll = ll1I1lll
    else:
        l1lII1ll = IlI1lI11
    if l1lII1ll == I11IlIII:
        if not I111I1ll._queueList:
            l1lII1ll = IIlll11I
        else:
            l1lII1ll = lllI1I1l
    if l1lII1ll == Ill1l1lI:
        Illll1Il = I1lllll1
    if l1lII1ll == IllI1IIl:
        Illll1Il = I1lIllll
    if Illll1Il == ll1IlIll:
        l1l11Il1 = IlII11I1
        if not IIll1I1I(l11I1l11, lIIIIII1):
            l1l11Il1 = ll1l1I11
        else:
            l1l11Il1 = IllI11Il
        if l1l11Il1 == Ill1I1lI:
            if not I111I1Il(IlI1IIll):
                l1l11Il1 = lIlI1l1l
            else:
                l1l11Il1 = I1lllll1
        if l1l11Il1 == I11IIlI1:
            Illll1Il = II1IIl1l
        if l1l11Il1 == IlI1lI11:
            Illll1Il = II1l1llI
    if Illll1Il == II1l1llI:
        pass
    if Illll1Il == I1I11l11:
        with lockguard.LockGuard(I111I1ll._queueListLock):
            I1Il1I11 = l1IIll11
            lI1I11I1 = III1ll1l
            if not I111I1ll._queueList:
                lI1I11I1 = Ill1l1lI
            else:
                lI1I11I1 = IIlllIlI
            if lI1I11I1 == Ill1l1lI:
                if not IIlIIIIl.I111lIl1(l1III1Il):
                    lI1I11I1 = lllll1ll
                else:
                    lI1I11I1 = llI11Ill
            if lI1I11I1 == l11ll1Il:
                I1Il1I11 = l111l11I
            if lI1I11I1 == ll1IlIll:
                I1Il1I11 = lll1IIlI
            if I1Il1I11 == I11I11ll:
                llI1l111 = l1I1111l
                if not ll1lI1lI(lllI1I1l):
                    llI1l111 = I1l11l11
                else:
                    llI1l111 = Il11I1ll
                if llI1l111 == IIIIIIll:
                    if not lIIIIII1:
                        llI1l111 = l1IIl111
                    else:
                        llI1l111 = IIllI11l
                if llI1l111 == IIllI11l:
                    I1Il1I11 = l111I111
                if llI1l111 == lIlIl11I:
                    I1Il1I11 = Ill1I1lI
            if I1Il1I11 == l1I1IIIl:
                pass
            if I1Il1I11 == lIl1l1ll:
                lIllll1l = I111I1ll._queueList[l1I1I11I]
                I111I1ll._queueList = I111I1ll._queueList[lI1I1l1I:]
                return lIllll1l
    return lIl11lIl

def I1I1I111(l1IlllI1):
    return not l1IlllI1.emptyQueue() and l1IlllI1._doCanNotifyQueueAvailable()

def llI1I11I(Il1IIl11):
    return not I1Il1lIl(Il1IIl11._queueNotifyCounter, l1I1I11I)

class EventQueue(eventdispatcher.EventDispatcher):

    def __init__(self, policy=eventpy.policy.defaultPolicy):
        (IIlIlIlI, l1lIIII1) = (policy, self)
        super().__init__(IIlIlIlI)
        l1lIIII1._policy = IIlIlIlI.clone()
        l1lIIII1._queueListLock = l1lIIII1._policy.lockClass()
        l1lIIII1._queueNotifyCounter = lI1IllI1
        l1lIIII1._queueEmptyCounter = lI1IllI1
        l1lIIII1._queueList = []
        l1lIIII1._queueListMutex = l1lIIII1._policy.lockClass()
        l1lIIII1._queueListConditionVariable = l1lIIII1._policy.conditionClass(l1lIIII1._queueListMutex)

    def enqueue(self, *args, **kwargs):
        return II1IlI1I(self, *args, **kwargs)

    def emptyQueue(self):
        return IIIlll11(self)

    def clearEvents(self):
        return I1llll1l(self)

    def process(self):
        return I1111lII(self)

    def processOne(self):
        return llI1IIll(self)

    def processIf(self, func):
        return lll1IIII(self, func)

    def wait(self):
        return l1l11l1I(self)

    def waitFor(self, seconds):
        return l11lIII1(self, seconds)

    def dispatchEvent(self, queuedEvent):
        return II11Il1l(queuedEvent, self)

    def peekEvent(self):
        return I1llIlll(self)

    def takeEvent(self):
        return l1l11Ill(self)

    def _doCanProcess(self):
        return I1I1I111(self)

    def _doCanNotifyQueueAvailable(self):
        return llI1I11I(self)