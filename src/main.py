from typing import List
import click
from datetime import datetime, date
from commands.download_hotel_prices import DownloadPrices
from commands.find_offers import FindOffers, HotelOffer
from commands.download_tickets_prices import DownloadTicketPrices
from commands.send_offers import send_offers_by_email

@click.group()
def cli():
    pass

@cli.command()
@click.option('--date-ini', type=click.DateTime(formats=["%Y-%m-%d"]), default=str(date.today()), help='Start date in YYYY-MM-DD format')
@click.option('--date-end', type=click.DateTime(formats=["%Y-%m-%d"]), help='End date in YYYY-MM-DD format')
@click.option('--children', default=2, type=int, help='Number of children')
@click.option('--children-ages', default="6,9", type=str, help='Ages of children (comma-separated)')
@click.option('--adults', default=2, type=int, help='Number of adults')
@click.option('--file-sufix', default="", type=str, help='Export filename sufix')
def download_rates(date_ini: datetime, 
                   date_end: datetime, 
                   children: int,
                   children_ages: str,
                   adults: int,
                   file_sufix: str): 
    
    dtp = DownloadTicketPrices()
    dtp.download_and_save_to_file()

    dp = DownloadPrices(date_ini=date_ini, 
                        date_end=date_end,
                        children = children,
                        children_ages=children_ages,
                        adults=adults,
                        file_sufix=file_sufix)
    dp.download()
    click.echo("Rates downloaded successfully.")


@cli.command()
def download_ticket_prices():
    dtp = DownloadTicketPrices()
    dtp.download()


@cli.command()
@click.option('--hotel-prices', type=click.Path(exists=True), help='Path to the hotel prices file')
@click.option('--ticket-prices', type=click.Path(exists=True), help='Path to the ticket prices file')
@click.option('--date-ini', required=False, type=click.DateTime(formats=["%Y-%m-%d"]), help='Start date in YYYY-MM-DD format')
@click.option('--date-end', required=False, type=click.DateTime(formats=["%Y-%m-%d"]), help='End date in YYYY-MM-DD format')
@click.option('--send-email', required=False, type=bool, default=False, help='Send email with offers')
def find_offers(hotel_prices:str, 
                ticket_prices:str, 
                date_ini:datetime, 
                date_end:datetime,
                send_email:bool):
    find_offers_instance = FindOffers(hotel_prices_file=hotel_prices,
                                      ticket_prices_file=ticket_prices,
                                      date_ini=date_ini, 
                                      date_end=date_end)


    

    find_offers_instance.print_unique_hotel_names()
    click.echo("----------------------------------")
    # find_offers_instance.print_last_date_with_rate()
    # print("-------------Lowest rates all hotels:---------------")
    # find_offers_instance.print_minor_rates_all_hotels()
    # print("-------------Lowest rates only Portaventura hotels:---------------")
    # offers = find_offers_instance.get_minor_rates_only_port_aventura()
    
    
    body = 'Here are the latest portaventura offers:\n'

    offers = find_offers_instance.get_minor_rates_only_this_hotel("Hotel Roulette")
    body += append_to_body(offers=offers, hotel_name="Hotel Roulette")
    
    offers = find_offers_instance.get_minor_rates_only_this_hotel("Hotel Caribe")
    body += append_to_body(offers=offers, hotel_name="Hotel Caribe")

    offers = find_offers_instance.get_minor_rates_only_this_hotel("Deluxe Superior Club San Juan")
    body += append_to_body(offers=offers, hotel_name="Deluxe Superior Club San Juan")

    offers = find_offers_instance.get_minor_rates_only_this_hotel("Hotel Mansión de Lucy")
    body += append_to_body(offers=offers, hotel_name="Hotel Mansión de Lucy")

    offers = find_offers_instance.get_minor_rates_only_this_hotel("Hotel Colorado Creek")
    body += append_to_body(offers=offers, hotel_name="Hotel Colorado Creek")

    offers = find_offers_instance.get_minor_rates_only_this_hotel("Deluxe Colorado")
    body += append_to_body(offers=offers, hotel_name="Deluxe Colorado")

    offers = find_offers_instance.get_minor_rates_only_this_hotel("Hotel Gold River")
    body += append_to_body(offers=offers, hotel_name="Hotel Gold River")

    offers = find_offers_instance.get_minor_rates_only_this_hotel("Hotel PortAventura")
    body += append_to_body(offers=offers, hotel_name="Hotel PortAventura")

    offers = find_offers_instance.get_minor_rates_only_this_hotel("Hotel El Paso")
    body += append_to_body(offers=offers, hotel_name="Hotel El Paso")

    print(body)

    if send_email == True:
        send_offers_by_email(body = body)

def append_to_body(offers: List[HotelOffer], hotel_name: str) -> str:
    body = f"\n\n-------------Lowest rates {hotel_name}:---------------\n"
    for offer in offers:
        body += f"Date: {offer.date} ({offer.day_of_week})({offer.occupancy})({offer.occupancy_next_day}), Hotel Name: {offer.name}, Rate: {offer.rate}\n"
    return body

if __name__ == '__main__':
    cli()
