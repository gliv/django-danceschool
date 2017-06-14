# Give this app a custom verbose name to avoid confusion
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from danceschool.core.utils.sys import isPreliminaryRun


class FinancialAppConfig(AppConfig):
    name = 'danceschool.financial'
    verbose_name = _('Financial Functions')

    def ready(self):
        from django.core.exceptions import ValidationError
        from django.db import connection

        from danceschool.core.models import Event, SubstituteTeacher, Invoice, InvoiceItem
        from danceschool.core.constants import getConstant, updateConstant

        # Add some properties to Invoices that are useful for the check-in process.
        # to ensure that the financials are being recorded correctly.

        @property
        def revenueReportedGross(self):
            if hasattr(self,'revenueitem') and self.revenueitem:
                return self.revenueitem.total
            return 0
        InvoiceItem.add_to_class('revenueReportedGross',revenueReportedGross)

        @property
        def revenueReported(self):
            if hasattr(self,'revenueitem') and self.revenueitem:
                return self.revenueitem.netRevenue
            return 0
        InvoiceItem.add_to_class('revenueReported',revenueReported)

        @property
        def feesReported(self):
            if hasattr(self,'revenueitem') and self.revenueitem:
                return self.revenueitem.fees
            return 0
        InvoiceItem.add_to_class('feesReported',feesReported)

        @property
        def taxesReported(self):
            if hasattr(self,'revenueitem') and self.revenueitem:
                return self.revenueitem.taxes
            return 0
        InvoiceItem.add_to_class('taxesReported',taxesReported)

        @property
        def revenueReceivedGross(self):
            if hasattr(self,'revenueitem') and self.revenueitem and self.revenueitem.received:
                return self.revenueitem.total
            return 0
        InvoiceItem.add_to_class('revenueReceivedGross',revenueReceivedGross)

        @property
        def revenueReceived(self):
            if hasattr(self,'revenueitem') and self.revenueitem and self.revenueitem.received:
                return self.revenueitem.netRevenue
            return 0
        InvoiceItem.add_to_class('revenueReceived',revenueReceived)

        @property
        def revenueMismatch(self):
            comparison = self.revenueReported + self.revenueRefundsReported
            if not getConstant('registration__buyerPaysProcessingFees'):
                comparison += self.feesReported
            if not getConstant('registration__buyerPaysSalesTax'):
                comparison += self.taxesReported

            return round(self.total,2) != round(comparison,2)
        InvoiceItem.add_to_class('revenueMismatch',revenueMismatch)

        @property
        def invoiceRevenueMismatch(self):
            for x in self.invoiceitem_set.all():
                if x.revenueMismatch:
                    return True

            return False
        Invoice.add_to_class('revenueMismatch', invoiceRevenueMismatch)

        @property
        def revenueNotYetReceived(self):
            return self.revenueReceived != self.revenueReported
        InvoiceItem.add_to_class('revenueNotYetReceived',revenueNotYetReceived)

        @property
        def invoiceRevenueNotYetReceived(self):
            for x in self.invoiceitem_set.all():
                if x.revenueNotYetReceived:
                    return True

            return False
        Invoice.add_to_class('revenueNotYetReceived', invoiceRevenueNotYetReceived)

        @property
        def revenueRefundsReported(self):
            if hasattr(self,'revenueitem') and self.revenueitem:
                return -1 * self.revenueitem.adjustments
            return 0
        InvoiceItem.add_to_class('revenueRefundsReported',revenueRefundsReported)

        @property
        def invoiceRevenueRefundsReported(self):
            return sum([x.revenueRefundsReported for x in self.invoiceitem_set.all()])
        Invoice.add_to_class('revenueRefundsReported', invoiceRevenueRefundsReported)

        # Add a property and a validator to check for and validate that teachers have not
        # already been paid when accepting SubstituteTeacher submissions.
        @property
        def paidOut(self):
            ''' Add a property to Series indicating whether it has been paid out. '''
            return (True in self.expenseitem_set.filter(eventstaffmember__isnull=False).values_list('paid',flat=True))
        Event.add_to_class('paidOut', paidOut)

        def validate_EnsureNotPaidOut(event_pk):
            ''' Add a validator to SubstituteTeacher submissions checking if the series has been paid out '''
            event = Event.objects.get(pk=event_pk)
            if event.paidOut:
                raise ValidationError(_('Staff members for this series have already been paid.  If you need to adjust hours worked, you will need to request money from them directly.'))

        for field in [f for f in SubstituteTeacher._meta.fields if f.name == 'event']:
            field.validators.append(validate_EnsureNotPaidOut)

        # This ensures that the receivers are loaded.
        from . import handlers

        # Add get_or_create calls to ensure that the Expense and Revenue categories needed
        # for our handlers exist.  Other categories can always be created, and these can be
        # modified in the database.
        if 'financial_expensecategory' in connection.introspection.table_names() and not isPreliminaryRun():
            ExpenseCategory = self.get_model('ExpenseCategory')

            # Name, preference key, and defaultRate
            new_expense_cats = [
                (_('Class Instruction'),'financial__classInstructionExpenseCatID',0),
                (_('Assistant Class Instruction'),'financial__assistantClassInstructionExpenseCatID',0),
                (_('Other Event-Related Staff Expenses'),'financial__otherStaffExpenseCatID',0),
                (_('Venue Rental'),'financial__venueRentalExpenseCatID',None),
            ]

            for cat in new_expense_cats:
                if (getConstant(cat[1]) or 0) <= 0:
                    new_cat, created = ExpenseCategory.objects.get_or_create(
                        name=cat[0],
                        defaults={'defaultRate': cat[2]},
                    )
                    # Update constant and fail silently
                    updateConstant(cat[1],new_cat.id,True)

        if 'financial_revenuecategory' in connection.introspection.table_names() and not isPreliminaryRun():
            RevenueCategory = self.get_model('RevenueCategory')

            # Name and preference key
            new_revenue_cats = [
                (_('Registrations'),'financial__registrationsRevenueCatID'),
                (_('Purchased Vouchers/Gift Certificates'),'financial__giftCertRevenueCatID'),
                (_('Unallocated Online Payments'),'financial__unallocatedPaymentsRevenueCatID'),
            ]

            for cat in new_revenue_cats:
                if (getConstant(cat[1]) or 0) <= 0:
                    new_cat, created = RevenueCategory.objects.get_or_create(name=cat[0])
                    # Update constant and fail silently
                    updateConstant(cat[1],new_cat.id,True)
