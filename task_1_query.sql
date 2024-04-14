select sum(case
when c.currency_code = 'EUR' then p.amount
else p.amount * r.exchange_rate_to_eur
end) as total_amount_in_eur, p.transaction_date
from payments p 
left join currency_rates r on p.currency = r.currency_id and p.transaction_date = r.exchange_date
left join currencies c on c.currency_id = p.currency
left join blacklist b on p.user_id_sender = b.user_id
where (b.user_id is null 
or not(b.blacklist_start_date < p.transaction_date 
and (b.blacklist_end_date > p.transaction_date 
or b.blacklist_end_date is null)))
and c.end_date is null
group by transaction_date