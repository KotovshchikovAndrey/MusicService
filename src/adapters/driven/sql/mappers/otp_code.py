from datetime import UTC

from adapters.driven.sql.models.otp_code import OTPCode as OTPCodeModel
from domain.models.entities.otp_code import OTPCode


def map_to_otp_code(otp_code_model: OTPCodeModel) -> OTPCode:
    return OTPCode(
        id=otp_code_model.id,
        code=otp_code_model.code,
        owner_id=otp_code_model.owner_id,
        expired_at=otp_code_model.expired_at.replace(tzinfo=UTC),
        purpose=otp_code_model.purpose,
    )


def map_to_insert_otp_code_values(otp_code: OTPCode) -> dict:
    return {
        "id": otp_code.id,
        "code": otp_code.code,
        "owner_id": otp_code.owner_id.hex,
        "purpose": otp_code.purpose.value,
        "expired_at": otp_code.expired_at.replace(tzinfo=None),
    }
