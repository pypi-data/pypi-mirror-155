class Node:
 def __init__(self, data):
      self.left = None
      self.right = None
      self.data = data
 def insert(self, root,nd):
       if nd.data>root.data:
           if root.right is None:
               root.right=nd
           else:
               self.insert(root.right,nd)
       if nd.data<root.data:
           if root.left is None:
               root.left=nd
           else:
               self.insert(root.left,nd)
 def binarysearch(self,root,nd):
        if nd.data>root.data:
           #print(root.data,end=" ")
           printvia(root.data)
           self.binarysearch(root.right,nd)
        if nd.data<root.data:
           printvia(root.data)
           #print(root.data,end=" ")
           self.binarysearch(root.left,nd)
        if nd.data==root.data:
           printvia(root.data)
           #print(root.data,end=" ")
root=Node(350)
def nodeadder(r,index):
	root.insert(r,Node(index))
placeindex=[200,800,100,300,780,900,50,150,250,320,750,790,850,950,60,75,125,160,225,270,310,325,700,765,785,795,825,875,925,975,25,45,55,80,120,130,155,165,220,230,260,275,305,315,325,330,650,720,760,770,820,830,860,880]
for i in range(len(placeindex)):
    nodeadder(root,placeindex[i])
def printvia(via):
    if(via==350):
        print("Peelamedu -",end=" ")
    if (via == 200):
        print("Nava India -", end=" ")
    if (via == 800):
        print("Airport -", end=" ")
    if (via == 100):
        print("Siddhapudhur -", end=" ")
    if (via == 300):
        print("Lakshmi Mills -", end=" ")
    if (via == 780):
        print("Sitra -", end=" ")
    if (via == 900):
        print("Goldwins -", end=" ")
    if (via == 50):
        print("Gandhipark -", end=" ")
    if (via == 150):
        print("Gandhipuram -", end=" ")
    if (via == 250):
        print("Racecourse -", end=" ")
    if (via == 320):
        print("Ramanathapuram -", end=" ")
    if (via == 750):
        print("Nehru Nagar -", end=" ")
    if (via == 790):
        print("Thottipalayam -", end=" ")
    if (via == 850):
        print("Chinniampalayam -", end=" ")
    if (via == 950):
        print("Neelambur -", end=" ")
    if (via == 40):
        print("Rathnapuri -", end=" ")
    if (via == 75):
        print("Sivanandha Colony -", end=" ")
    if (via == 125):
        print("Brookefields -", end=" ")
    if (via == 160):
        print("Nehru Stadium -", end=" ")
    if (via == 225):
        print("Government Hospital -", end=" ")
    if (via == 270):
        print("Sungam -", end=" ")
    if (via == 310):
        print("Nanjundapuram -", end=" ")
    if (via == 325):
        print("Singanallur -", end=" ")
    if (via == 700):
        print("Kalapatti -", end=" ")
    if (via == 765):
        print("Vilankurichi -", end=" ")
    if (via == 785):
        print("Thee Spot Resorts -", end=" ")
    if (via == 795):
        print("Vellanaipatti -", end=" ")
    if (via == 825):
        print("Irugur -", end=" ")
    if (via == 875):
        print("Pappampatti Pirivu -", end=" ")
    if (via == 925):
        print("Maharaja Theme Park -", end=" ")
    if (via == 975):
        print("PSG ITech -", end=" ")
    if (via == 25):
        print("Sanganoor -", end=" ")
    if (via == 45):
        print("Manayakaram Palayam -", end=" ")
    if (via == 80):
        print("Vellakinar -", end=" ")
    if (via == 120):
        print("Saibaba Colony -", end=" ")
    if (via == 130):
        print("RS Puram -", end=" ")
    if (via == 155):
        print("Railway Station -", end=" ")
    if (via == 220):
        print("Townhall -", end=" ")
    if (via == 230):
        print("Valankulam -", end=" ")
    if (via == 260):
        print("Ukkadam -", end=" ")
    if (via == 275):
        print("Kottaipudur -", end=" ")
    if (via == 305):
        print("Sundarapuram -", end=" ")
    if (via == 315):
        print("Podanur -", end=" ")
    if (via == 323):
        print("Vellalur -", end=" ")
    if (via == 330):
        print("Ondipudur -", end=" ")
    if (via == 650):
        print("Kurumbapalayam -", end=" ")
    if (via == 720):
        print("Telungupalayam -", end=" ")
    if (via == 760):
        print("Saravanampatti -", end=" ")
    if (via == 770):
        print("Keeranatham -", end=" ")
    if (via == 820):
        print("L&T Bye-Pass -", end=" ")
    if (via == 830):
        print("Pattanam Pudur -", end=" ")
    if (via == 860):
        print("Nadupalayam Pirivu -", end=" ")
    if (via == 880):
        print("Sulur -", end=" ")
def startmap():
    print("\t\t\t\t\t\t\t\t\tCoimbatore Map\nPeelamedu(350)\t|\tNavaIndia(200)\t|\tAirport(800)\t|\tSiddhapudhur(100)\t|\tLakshmiMills(300)\t|\tSitra(780)",end="\n")
    print("Goldwins(900)\t|\tGandhipark(50)\t|\tGandhipuram(150)\t|\tRacecourse(250)\t|\tRamanathapuram(320)",end="\n")
    print("Nehru Nagar(750)\t|\tThottipalayam(790)\t|\tChinniampalayam(850)\t|\tNeelambur(950)\t|\tRathnapuri(40)",end="\n")
    print("Sivanandha Colony(75)\t|\tBrookeFields(125)\t|\tNehru Stadium(160)\t|\tGovernment Hospital(225)\t|\tSungam(270)",end="\n")
    print("Nanjundapuram(310)\t|\tSinganallur(325)\t|\tKalapatti(700)\t|\tVilankurichu(765)\t|\tThee Spot Resorts(785)",end="\n")
    print("Vellanaipatti(795)\t|\tIrugur(825)\t|\tPappampatti Pirivu(875)\t|\tMaharaja Theme Park(925)\t|\tPSG ITech(975)",end="\n")
    print("Sanganoor(25)\t|\tManayakaram Palayam(45)\t|\tKoundampalayam(55)\t|\tVellakinar(80)\t|\tSaibaba Colony(120)",end="\n")
    print("RS Puram(130)\t|\tRailway Station(155)\t|\tTownhall(220)\t|\tValankulam(230)\t|\tUkkadam(260)",end="\n")
    print("Kottaipudur(275)\t|\tSundarapuram(305)\t|\tPodanur(315)\t|\tVellalur(323)\t|\tOndipudur(330)",end="\n")
    print("Kurumbapalayam(650)\t|\tThelungapalayam(720)\t|\tSaravanampatti(760)\t|\tKeeranatham(770)\t|\tL&T Bye-Pass Road",end="\n")
    print("Pattanam Pudur(830)\t|\tNadupalayam Pirivu(860)\t|\tSulur(880)")
    target=int(input("\nYour current location is Peelamedu(350)\nEnter the Destination's Code : "))
    root.binarysearch(root,Node(target))