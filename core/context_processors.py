from .models import CompanyInfo

def company_info(request):
    """
    Context processor to make company info available in all templates
    """
    try:
        company = CompanyInfo.objects.first()
    except:
        company = None
    
    return {
        'company_info': company
    }
