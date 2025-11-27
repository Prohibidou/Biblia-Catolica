import sqlite3
import gzip
import shutil
import os

# Complete text for Jude commentary
jude_comment = """Saludo y bendición: Judas, siervo de Jesucristo y hermano de Santiago, a los que han recibido la llamada divina, amados de Dios Padre y guardados para Jesucristo: misericordia, paz y amor en abundancia para vosotros.

Motivo de la carta: Como tengo gran interés en escribiros sobre nuestra común salvación, me siento obligado a dirigiros esta carta, para exhortaros a combatir por la fe que ha sido entregada a los santos de una vez por todas. Porque se han infiltrado ciertos hombres, ya desde hace tiempo señalados en la Escritura para esta condenación, hombres impíos que convierten en libertinaje la gracia de nuestro Dios y niegan al único Dueño y Señor nuestro, Jesucristo.

I. DENUNCIA DE LOS FALSOS MAESTROS - El castigo que espera a esos impíos: El Señor —después de haber salvado al pueblo de la tierra de Egipto— hizo perecer a continuación a los que no creyeron; y que a los ángeles que no guardaron su dignidad, sino que abandonaron su propia morada, los tiene guardados en tinieblas con cadenas eternas para el juicio del gran día; también Sodoma y Gomorra y las ciudades vecinas, que como ellos se entregaron a la fornicación y siguieron un uso antinatural de la carne, están puestas para escarmiento, sufriendo el castigo de un fuego eterno.

Su conducta inmoral y escandalosa: También éstos, a pesar de todo, en su delirio manchan su cuerpo, desprecian la autoridad del Señor y blasfeman contra los seres gloriosos. El arcángel Miguel, cuando —oponiéndose al diablo— disputaba sobre el cuerpo de Moisés, no se atrevió a pronunciar una sentencia injuriosa, sino que dijo: ¡Que el Señor te reprenda! Pero éstos blasfeman contra todo lo que desconocen; y en lo que conocen por instinto natural como las bestias irracionales, en eso se corrompen. ¡Ay de ellos!, porque se metieron por el camino de Caín, y se precipitaron por afán de lucro en la aberración de Balaán, y perecieron en la rebelión de Coré. Éstos son una mancha en vuestros ágapes: comportándose sin recato como si estuvieran en banquetes, se cuidan a sí mismos; son nubes sin agua zarandeadas por los vientos; árboles de otoño sin fruto, dos veces muertos y arrancados de raíz; olas bravías del mar que echan la espuma de sus torpezas; astros errantes a los que está reservada para siempre la oscuridad tenebrosa.

El juicio de Dios: De ellos también profetizó Henoc, el séptimo descendiente de Adán, cuando dijo: «Mira, ha venido el Señor con sus santas miríadas, para entablar juicio contra todos y dejar convictos a todos los impíos de todas las perversidades que han cometido, y de todas las injurias que los pecadores impíos han proferido contra él». Éstos son unos murmuradores que se quejan de su suerte, viviendo al dictado de sus concupiscencias; y su boca pronuncia palabras hinchadas, adulando a las personas por su propio interés.

II. EXHORTACIONES A LOS FIELES - Estaba predicha la aparición de los impíos: Acordaos de las palabras anunciadas por medio de los apóstoles de nuestro Señor Jesucristo, que os decían: «En los últimos tiempos habrá quienes se burlen de todo y vivan según sus impías concupiscencias». Éstos son los que crean divisiones, hombres meramente naturales, que no tienen el Espíritu.

Las virtudes teologales: Edificándoos sobre vuestra santísima fe y orando en el Espíritu Santo, manteneos en el amor de Dios, aguardando que la misericordia de nuestro Señor Jesucristo os conceda la vida eterna.

Comportamiento con los que vacilan: Tratad con compasión a los que vacilan: a unos procurad salvarlos, arrancándolos del fuego; a otros tratadlos con misericordia, pero con precaución, aborreciendo hasta la túnica contaminada por su carne.

Doxología final: Al que es poderoso para guardaros sin tropiezo y presentaros sin tacha y con júbilo delante de su gloria, al único Dios, Salvador nuestro por medio de Jesucristo nuestro Señor, la gloria, la majestad, el imperio y la potestad, desde siempre y ahora y por todos los siglos. Amén."""

# Complete text for Philemon commentary
philemon_comment = """Saludo: Pablo, prisionero de Cristo Jesús, y Timoteo, el hermano, a Filemón, nuestro querido amigo y colaborador, a Apfia, la hermana, a Arquipo, nuestro compañero de armas, y a la iglesia que se reúne en tu casa: la gracia y la paz de Dios, nuestro Padre, y del Señor Jesucristo estén con vosotros.

Acción de gracias: Doy gracias sin cesar a mi Dios recordándote en mis oraciones, porque conozco la caridad y la fe que tienes en Jesús, el Señor, y en todos los santos. Que tu participación en la misma fe llegue a ser activa al comprender que todo el bien que tenemos es para Cristo. Pues, en verdad, he tenido gran alegría y consuelo por tu caridad, porque, gracias a ti, hermano, los corazones de los santos han encontrado alivio.

Intercesión en favor de Onésimo: Aun teniendo plena libertad en Cristo para mandarte lo que conviene, prefiero rogar en nombre de la caridad —y eso que soy Pablo, ya anciano y ahora además prisionero de Cristo Jesús—. Te ruego en favor de mi hijo Onésimo, a quien engendré entre cadenas, en otro tiempo inútil para ti pero ahora útil para ti y para mí: a éste te lo devuelvo como si fuera mi corazón. Yo hubiera querido retenerlo para que me sirviera en tu lugar, mientras estoy entre cadenas por el Evangelio.

Pero no he querido hacer nada sin tu consentimiento, para que tu buena acción no sea forzada, sino voluntaria. Quizá por eso se alejó algún tiempo, para que ahora lo recuperes para siempre, no ya como siervo, sino más que siervo, como hermano muy amado, en primer lugar para mí, pero ¡cuánto más para ti!, no sólo en lo humano, sino también en el Señor.

Por tanto, si me consideras hermano en la fe, acógelo como si fuera yo mismo. Si te perjudicó o te debe algo, cárgalo a mi cuenta. Yo, Pablo, lo he escrito de mi puño y letra; yo te pagaré, por no decirte que tú mismo te me debes. Sí, hermano, que yo reciba de ti este gozo en el Señor. Consuela en Cristo mi corazón. Te escribo confiando en tu obediencia, porque sé que harás aun más de lo que te digo.

Últimas recomendaciones y saludos: Además, prepárame hospedaje, pues espero que, gracias a vuestras oraciones, se me conceda estar entre vosotros. Te saludan Epafras, compañero de mi cautiverio en Cristo Jesús, y mis colaboradores Marcos, Aristarco, Demas y Lucas. La gracia del Señor Jesucristo esté con vuestro espíritu."""

print("Adding complete commentary to Jude and Philemon...")

# Decompress
gz_path = "public/bibles/navarra.sqlite.gz"
db_path = "scripts/temp_add_jude_phm.sqlite"

with gzip.open(gz_path, 'rb') as f_in:
    with open(db_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add Jude commentary to all verses in Jude
cursor.execute("UPDATE verses SET comment = ? WHERE book = 'JUD'", (jude_comment,))
jude_updated = cursor.rowcount
print(f"Updated {jude_updated} verses in Jude with commentary")

# Add Philemon commentary to all verses in Philemon  
cursor.execute("UPDATE verses SET comment = ? WHERE book = 'PHM'", (philemon_comment,))
phm_updated = cursor.rowcount
print(f"Updated {phm_updated} verses in Philemon with commentary")

# Verify
cursor.execute("SELECT COUNT(*) FROM verses WHERE book = 'JUD' AND comment IS NOT NULL AND comment != ''")
jude_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM verses WHERE book = 'JUD'")
jude_total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM verses WHERE book = 'PHM' AND comment IS NOT NULL AND comment != ''")
phm_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM verses WHERE book = 'PHM'")
phm_total = cursor.fetchone()[0]

print(f"\nVerification:")
print(f"JUD: {jude_count}/{jude_total} verses now have comments")
print(f"PHM: {phm_count}/{phm_total} verses now have comments")

conn.commit()
conn.close()

# Recompress
print("\nRecompressing database...")
with open(db_path, 'rb') as f_in:
    with gzip.open(gz_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

os.remove(db_path)
print("Done!")
