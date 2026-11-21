"""Ver.3 editorial ledger. Source times are the earliest verified for this edition."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Story:
    id: str
    where: str
    beat: str
    headline: str
    detail: str
    source: str
    url: str
    first_verified: str
    figure: str = ""
    figure_label: str = ""
    event_date: str = "2026-11-20 (local)"
    status: str = "verified against cited source"


LEADS = (
    Story("kyiv", "Kyiv, Ukraine / E. Poland", "Security",
          "Russian strikes hit\nKyiv bridges",
          "Three Kyiv bridges were hit. Russian missiles also fell in Poland; NATO called it an airspace breach.",
          "AP", "https://apnews.com/article/433e18f00cbd37a2a9da94e60fce0e07",
          "2026-11-20 08:31 UTC (AP coverage)", "3", "Kyiv bridges hit"),
    Story("cop31", "Antalya, Türkiye", "Climate",
          "COP31 goes\ninto overtime",
          "UN climate talks ran past their deadline. Delegates and activists criticized a draft that omitted fossil fuels.",
          "The Guardian", "https://www.theguardian.com/environment/2026/nov/20/cop31-talks-overtime-fossil-fuels-vanish-from-draft-deal",
          "2026-11-20 18:56 UTC"),
    Story("nuclear", "Washington, U.S.", "Diplomacy",
          "Trump warns of China’s\nnuclear buildup",
          "He spoke a day after the U.S., China and Russia pledged to discuss nuclear risks at their Shenzhen summit.",
          "AP", "https://apnews.com/article/286391edaacc7e8544dc0dc023e253fb",
          "2026-11-20 20:12 UTC"),
)


SECTIONS = (
    ("ECONOMY", (
        Story("stocks", "New York, U.S.", "Markets", "Wall Street’s tech rout deepens",
              "S&P 500 fell 3.7%; Nasdaq ended below its start-of-year level.",
              "AP", "https://apnews.com/article/c10b797a17c2acf37924d834efebe135",
              "2026-11-20 21:30 UTC (closing report)", "−3.7%", "S&P 500 daily close"),
        Story("japan", "Japan", "Inflation", "Core inflation accelerates",
              "October’s index excluding fresh food rose 2.2% year on year.",
              "Reuters", "https://www.streetinsider.com/Reuters/Japans%2Bcore%2Binflation%2Baccelerates%2Bin%2BOctober%2C%2Bcementing%2Brate%2Bhike%2Bexpectations/27377746.html",
              "2026-11-20 08:43 JST (Reuters wire)", "2.2%", "Japan core CPI, Oct. YoY"),
        Story("uk-eu", "Brussels, Belgium", "Trade", "UK and EU advance trade reset",
              "Leaders advanced work on food checks, carbon and youth mobility.",
              "EU Council", "https://www.consilium.europa.eu/en/meetings/international-summit/2026/11/20/",
              "2026-11-20 (joint statement; time unverified)"),
        Story("taiwan", "Taiwan", "Markets", "Short-selling curbs take effect",
              "The new limits followed a sharp stock sell-off the day before.",
              "Taipei Times", "https://www.taipeitimes.com/News/biz/archives/2026/11/20/2003868040",
              "2026-11-20 (effective date; announced Nov 19)"),
        Story("retail", "Great Britain", "Retail", "Retail sales rebound in October",
              "Volumes rose 0.7% from September as food-store sales climbed.",
              "ONS", "https://www.ons.gov.uk/businessindustryandtrade/retailindustry/bulletins/retailsales/october2026",
              "2026-11-20 07:00 GMT (official release)", "+0.7%", "Great Britain retail, Oct. MoM"),
        Story("chile", "Chile", "Currencies", "Chilean peso slides",
              "The currency fell 0.6% against the U.S. dollar on Friday.",
              "Reuters", "https://www.fidelity.com/news/article/international/202611201637RTRSNEWSCOMBINED_L2N4710YJ_1",
              "2026-11-20 16:37 EST (quoted market report)", "−0.6%", "Chilean peso vs. dollar"),
        Story("australia", "Australia", "Outlook", "Minister plays down recession risk",
              "Amanda Rishworth cited Treasury and central bank forecasts.",
              "ABC Australia", "https://www.abc.net.au/news/2026-11-20/federal-politics-live-blog-recession-concerns/107407116",
              "2026-11-20 (Australia; time unverified)"),
        Story("tax", "U.S. / overseas", "Tech policy", "Trump floats data-center tax",
              "He threatened a levy on U.S. firms building AI facilities abroad.",
              "AP", "https://apnews.com/article/f1ac03b73d13445400eeed8631d9d879",
              "2026-11-20 17:45 UTC"),
    )),
    ("POLITICS & CONFLICT", (
        Story("gaza", "Central Gaza", "Conflict", "Israeli strikes kill Palestinians",
              "Local hospitals reported deaths after multiple strikes.",
              "AP / Al Jazeera", "https://apnews.com/article/16c39c487a23b53b73c5eabb7f0fd57a",
              "2026-11-20 (this item’s time in the rolling report unverified)"),
        Story("yemen", "Saudi Arabia / Yemen", "Conflict", "Saudi coalition and Houthis trade fire",
              "The coalition said it hit Yemen and intercepted attacks in Saudi Arabia.",
              "AP", "https://apnews.com/article/16c39c487a23b53b73c5eabb7f0fd57a",
              "2026-11-20 (this item’s time in the rolling report unverified)"),
        Story("sudan", "Blue Nile, Sudan", "Civil war", "Blue Nile moves to mobilize troops",
              "The regional government announced a response to reported rebel gains.",
              "Sudan Tribune", "https://sudantribune.com/article/321473",
              "2026-11-20 (time unverified)"),
        Story("myanmar", "Naypyitaw, Myanmar", "Justice", "Myanmar rejects genocide ruling",
              "The government rejected the UN court’s finding on the Rohingya.",
              "AP", "https://apnews.com/article/c76dcb3f97c1077262f87e0cba01bb78",
              "2026-11-20 08:13 UTC"),
        Story("denmark", "Denmark", "Security", "Denmark says it foiled a plot",
              "Officials blamed Russian intelligence for a plot against a U.S.-Ukrainian citizen.",
              "AP", "https://apnews.com/article/03494b78067c9572120deac038addd23",
              "2026-11-20 17:24 UTC"),
        Story("iran", "U.S. / Iran", "Diplomacy", "Trump doubts terms of Iran deal",
              "He said Tehran wanted an agreement but would offer no terms he could accept.",
              "AP", "https://apnews.com/article/8fd6dcd6dc4a1a77437cedc4567fbee8",
              "2026-11-20 21:54 UTC"),
        Story("iraq", "Jurf al-Sakhar, Iraq", "Security", "Iraqi forces enter militia stronghold",
              "They set up a command post near a longtime Kataib Hezbollah base.",
              "AP", "https://apnews.com/article/16c39c487a23b53b73c5eabb7f0fd57a",
              "2026-11-20 (this item’s time in the rolling report unverified)"),
        Story("serbia", "Belgrade, Serbia", "Justice", "Belgrade mayor charged with assault",
              "Prosecutors accuse Aleksandar Sapic of injuring an opposition councillor.",
              "Al Jazeera", "https://www.aljazeera.com/news/2026/11/20/belgrade-mayor-charged-with-assaulting-opposition-politician-in-serbia",
              "2026-11-20 (time unverified)"),
    )),
    ("WORLD BRIEFS", (
        Story("peru", "Junín, Peru", "Earthquake", "M6.7 quake shakes central Andes",
              "The quake hit at 19:09 local time and was felt in Lima.",
              "INDECI / AP", "https://portal.indeci.gob.pe/emergencias/reporte-preliminar-n-o-1159-20-11-2026-coen-indeci-1940-horas-sismo-de-magnitud-6-7-con-epicentro-en-el-junin-junin/",
              "2026-11-20 19:40 PET (preliminary bulletin)", "M6.7", "Central Peru earthquake",
              "2026-11-20 19:09 PET / 2026-11-21 00:09 UTC"),
        Story("flood", "Central Florida, U.S.", "Weather", "Floodwater rises as rain eases",
              "Residents along the St. Johns River were urged to prepare to leave.",
              "AP", "https://apnews.com/article/46b14622b3ad77c32eb0182bfe8bc9f4",
              "2026-11-20 15:00 UTC"),
        Story("children", "South Africa", "Rights", "Charity urges child-first policy",
              "Save the Children SA called for more investment on World Children’s Day.",
              "Channel Africa", "https://www.channelafrica.co.za/channelafrica/news/save-the-children-sa-calls-for-child-rights-to-guide-policy-decisions/",
              "2026-11-20 22:14 (outlet’s displayed local time)"),
        Story("brazil", "Brazil", "Culture", "Brazil marks Black Awareness Day",
              "The national holiday honors Zumbi dos Palmares and Afro-Brazilian culture.",
              "MinC", "https://www.gov.br/cultura/pt-br/assuntos/noticias/minc-celebra-o-dia-da-consciencia-negra-com-acoes-afirmativas-e-programacao-cultural",
              "Official advance notice; observance on 2026-11-20"),
        Story("skating", "Helsinki, Finland", "Sport", "Mao Shimada leads short program",
              "The Japanese skater scored 79.06 at the Finlandia Trophy.",
              "AP", "https://abcnews.com/Sports/wireStory/japans-shimada-estonias-selevko-lead-finlandia-trophy-skating-138328765",
              "2026-11-20 10:42 (ABC display; zone unverified)", "79.06", "Shimada short program score"),
        Story("gupta", "New York, U.S.", "Courts", "Gupta sentenced over murder plot",
              "He got 235 months for plotting to kill Sikh activist Gurpatwant Singh Pannun.",
              "AP / U.S. DOJ", "https://apnews.com/article/862cf5a608b00694f2cc661ece763134",
              "2026-11-20 17:35 UTC (AP)", "235 mo", "Gupta prison sentence"),
        Story("mill", "Longview, U.S.", "Labor", "Mill inquiry cites safety lapses",
              "State investigators reported violations after May’s tank rupture killed 11.",
              "AP", "https://apnews.com/article/6af77574d682b601568412cf9b3570f2",
              "2026-11-20 20:21 UTC"),
        Story("rikers", "New York, U.S.", "Justice", "Rikers closure targeted for 2032",
              "The mayor’s plan relies on cutting the number of people held in jail.",
              "AP", "https://apnews.com/article/aaf05ad46f0a999a213f2613fe39f7dc",
              "2026-11-20 10:01 UTC", "2032", "Target year to close Rikers"),
    )),
)


FIGURE_ORDER = ("kyiv", "stocks", "japan", "peru", "gupta")
