# handlers/payments.py
# ────────────────────────────────────────────────────────────
#  Обработчики платежей Telegram Payments API.
#
#  Как работает:
#  1. Пользователь нажимает «Купить доступ»
#  2. Бот отправляет invoice (счёт)
#  3. Telegram присылает pre_checkout_query — подтверждаем
#  4. После оплаты приходит successful_payment — активируем
# ────────────────────────────────────────────────────────────

import logging

from aiogram import Router
from aiogram.types import (
    CallbackQuery,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)

from config import config
from database import add_subscription, get_subscription_expires
from keyboards import main_menu_keyboard

logger = logging.getLogger(__name__)
router = Router()


def _price_label() -> str:
    if config.currency == "RUB":
        return f"{config.subscription_price // 100} руб."
    return f"{config.subscription_price / 100:.2f} {config.currency}"


async def send_invoice(message: Message) -> None:
    """Отправить счёт на оплату. Вызывается из других хендлеров."""
    if not config.payment_provider_token:
        await message.answer(
            "⚠️ Платежи пока не настроены.\n"
            "Обратись к администратору для получения доступа."
        )
        return

    await message.answer_invoice(
        title="🔞 Доступ к 18+ контенту",
        description=(
            f"Полный доступ к разделам «Чат 18+» и «Фотографии 18+» "
            f"на {config.subscription_days} дней.\n\n"
            "✅ Чат с AI без ограничений\n"
            "✅ Эксклюзивные фотографии\n"
            "✅ Мгновенная активация"
        ),
        payload="subscription_18plus",
        provider_token=config.payment_provider_token,
        currency=config.currency,
        prices=[
            LabeledPrice(
                label=f"Подписка на {config.subscription_days} дней",
                amount=config.subscription_price,
            )
        ],
        is_flexible=False,
    )


# ── Callback: кнопка «Купить доступ» ─────────────────────────────────────────

@router.callback_query(lambda c: c.data == "buy_access")
async def callback_buy_access(callback: CallbackQuery) -> None:
    """Нажатие кнопки «Купить доступ» — отправляем счёт."""
    await callback.answer()
    await send_invoice(callback.message)


# ── Callback: кнопка «Что входит?» ───────────────────────────────────────────

@router.callback_query(lambda c: c.data == "subscription_info")
async def callback_subscription_info(callback: CallbackQuery) -> None:
    await callback.answer(
        f"Подписка на {config.subscription_days} дней: "
        "Чат 18+ и Фото 18+ без ограничений!",
        show_alert=True,
    )


# ── Pre-checkout: подтверждение перед списанием ───────────────────────────────

@router.pre_checkout_query()
async def pre_checkout_handler(query: PreCheckoutQuery) -> None:
    """
    Telegram присылает ПЕРЕД списанием средств.
    Обязательно ответить в течение 10 секунд.
    """
    try:
        if query.invoice_payload != "subscription_18plus":
            await query.answer(ok=False, error_message="Неверный товар. Попробуй ещё раз.")
            return

        await query.answer(ok=True)
        logger.info("Pre-checkout approved: user=%d", query.from_user.id)

    except Exception as exc:
        logger.exception("Pre-checkout error: %s", exc)
        await query.answer(ok=False, error_message="Ошибка. Попробуй позже.")


# ── Successful payment: платёж прошёл успешно ────────────────────────────────

@router.message(lambda msg: msg.successful_payment is not None)
async def successful_payment_handler(message: Message) -> None:
    """
    Срабатывает после успешного списания средств.
    Записываем подписку в БД и уведомляем пользователя.
    """
    payment = message.successful_payment

    try:
        await add_subscription(
            user_id=message.from_user.id,
            payment_id=payment.telegram_payment_charge_id,
            amount=payment.total_amount,
            currency=payment.currency,
            days=config.subscription_days,
        )

        expires = await get_subscription_expires(message.from_user.id)
        expires_str = expires.strftime("%d.%m.%Y") if expires else "—"

        await message.answer(
            f"🎉 <b>Оплата прошла успешно!</b>\n\n"
            f"✅ Доступ к 18+ контенту активирован\n"
            f"📅 Подписка действует до: <b>{expires_str}</b>\n\n"
            "Теперь тебе доступны «Чат 18+» и «Фотографии 18+» 🔥\n"
            "Возвращайся в меню и выбирай раздел! 👇",
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )

        logger.info(
            "Payment OK: user=%d, amount=%d %s, id=%s",
            message.from_user.id,
            payment.total_amount,
            payment.currency,
            payment.telegram_payment_charge_id,
        )

    except Exception as exc:
        logger.exception("Error saving subscription: %s", exc)
        await message.answer(
            "✅ Оплата прошла, но возникла ошибка при активации.\n"
            "Напиши администратору — доступ откроют вручную.",
            reply_markup=main_menu_keyboard(),
        )
