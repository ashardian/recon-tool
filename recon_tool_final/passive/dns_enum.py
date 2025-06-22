import dns.resolver

def enumerate(domain):
    results = {}
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8', '1.1.1.1']

    for rtype in ['A', 'MX', 'TXT', 'NS']:
        try:
            answers = resolver.resolve(domain, rtype, raise_on_no_answer=False)
            records = [r.to_text() for r in answers] if answers.rrset else []
            results[rtype] = records
        except Exception as e:
            results[rtype] = []
            results[f"{rtype}_error"] = str(e)

    return results

