import random
import pickle
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Substitua 'TOKEN_DO_SEU_BOT' pelo token de acesso fornecido pelo BotFather
TOKEN = 'TOKEN_DO_SEU_BOT'

# Nome do arquivo para a base de dados
DATABASE_FILE = 'participantes.pickle'

# Carregar participantes do arquivo pickle, ou criar um arquivo novo caso não exista
try:
    with open(DATABASE_FILE, 'rb') as f:
        participantes = pickle.load(f)
except FileNotFoundError:
    participantes = []

# Função para o comando /participar
def participar_command(update: Update, context: CallbackContext) -> None:
    participante = update.message.from_user.username
    if participante not in participantes:
        participantes.append(participante)
        update.message.reply_text(f"{participante} foi adicionado ao sorteio.")
        salvar_participantes()
    else:
        update.message.reply_text("Você já está participando do sorteio.")

# Função para o comando /sorteio
def sorteio_command(update: Update, context: CallbackContext) -> None:
    motivo = " ".join(context.args)  # Extrai o motivo do sorteio a partir dos argumentos
    update.message.reply_text(f"Sorteio criado! Motivo: {motivo}")

# Função para o comando /sortear
def sortear_command(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 1 and context.args[0].isdigit():
        num_ganhadores = int(context.args[0])
        if len(participantes) > 0 and num_ganhadores <= len(participantes):
            ganhadores = random.sample(participantes, num_ganhadores)
            update.message.reply_text(f"Parabéns aos ganhadores: {', '.join(ganhadores)}!")
        else:
            update.message.reply_text("Número inválido de ganhadores ou não há participantes suficientes para o sorteio.")
    else:
        update.message.reply_text("Uso incorreto do comando. Use /sortear <num_ganhadores>.")

# Função para o comando /ganhadores
def ganhadores_command(update: Update, context: CallbackContext) -> None:
    num_ganhadores = int(context.args[0])
    update.message.reply_text(f"O sorteio terá {num_ganhadores} ganhadores.")

# Função para o comando /fimsorteio
def fimsorteio_command(update: Update, context: CallbackContext) -> None:
    participantes.clear()
    salvar_participantes()
    update.message.reply_text("Sorteio finalizado! A lista de participantes foi reiniciada.")

# Função para salvar a lista de participantes no arquivo pickle
def salvar_participantes():
    with open(DATABASE_FILE, 'wb') as f:
        pickle.dump(participantes, f)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("participar", participar_command))
    dp.add_handler(CommandHandler("sorteio", sorteio_command, pass_args=True))
    dp.add_handler(CommandHandler("sortear", sortear_command, pass_args=True))
    dp.add_handler(CommandHandler("ganhadores", ganhadores_command, pass_args=True))
    dp.add_handler(CommandHandler("fimsorteio", fimsorteio_command))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
