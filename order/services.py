from pets.models import AdoptionRequest, RequestedPet, Adoption, AdoptionPet
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError


class AdoptionService:
    @staticmethod
    def create_adoption(user_id, adoption_request_id):
        """
        Converts an AdoptionRequest into a confirmed Adoption.
        Marks pets as adopted.
        """
        with transaction.atomic():
            adoption_request = AdoptionRequest.objects.get(pk=adoption_request_id)
            requested_pets = adoption_request.requested_pets.select_related('pet').all()

            if not requested_pets:
                raise ValidationError({"detail": "No pets in adoption request"})

            adoption = Adoption.objects.create(user_id=user_id)

            adoption_pets = []
            for item in requested_pets:
                if item.pet.is_adopted:
                    raise ValidationError({"detail": f"Pet '{item.pet.name}' is already adopted"})
                
                adoption_pets.append(
                    AdoptionPet(
                        adoption=adoption,
                        pet=item.pet,
                        quantity=item.quantity
                    )
                )
                # Mark pet as adopted
                item.pet.is_adopted = True
                item.pet.save()

            AdoptionPet.objects.bulk_create(adoption_pets)

            # Delete the adoption request after adoption
            adoption_request.delete()

            return adoption

    @staticmethod
    def cancel_adoption(adoption, user):
        """
        Allows user or admin to cancel an adoption.
        """
        if user.is_staff:
            adoption.status = Adoption.CANCELED
            adoption.save()
            return adoption

        if adoption.user != user:
            raise PermissionDenied({"detail": "You can only cancel your own adoption"})

        if adoption.status == Adoption.COMPLETED:
            raise ValidationError({"detail": "You cannot cancel a completed adoption"})

        adoption.status = Adoption.CANCELED
        adoption.save()

        # Optional: mark pets as available again
        for item in adoption.adopted_pets.all():
            item.pet.is_adopted = False
            item.pet.save()

        return adoption
