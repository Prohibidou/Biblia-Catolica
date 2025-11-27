import sqlite3
import gzip
import shutil
import os

# Parsed comments for Jude - each section to specific verses
jude_comments = {
    # Saludo y bendición (1-2)
    (1, 1): "Saludo y bendición: Judas, siervo de Jesucristo y hermano de Santiago, a los que han recibido la llamada divina, amados de Dios Padre y guardados para Jesucristo.",
    (1, 2): "Misericordia, paz y amor en abundancia para vosotros.",
    
    # Motivo de la carta (3-4)
    (1, 3): "Motivo de la carta: Como tengo gran interés en escribiros sobre nuestra común salvación, me siento obligado a dirigiros esta carta, para exhortaros a combatir por la fe que ha sido entregada a los santos de una vez por todas.",
    (1, 4): "Porque se han infiltrado ciertos hombres, ya desde hace tiempo señalados en la Escritura para esta condenación, hombres impíos que convierten en libertinaje la gracia de nuestro Dios y niegan al único Dueño y Señor nuestro, Jesucristo.",
    
    # I. DENUNCIA DE LOS FALSOS MAESTROS - El castigo que espera a esos impíos (5-7)
    (1, 5): "I. DENUNCIA DE LOS FALSOS MAESTROS - El castigo que espera a esos impíos: El Señor —después de haber salvado al pueblo de la tierra de Egipto— hizo perecer a continuación a los que no creyeron.",
    (1, 6): "Y que a los ángeles que no guardaron su dignidad, sino que abandonaron su propia morada, los tiene guardados en tinieblas con cadenas eternas para el juicio del gran día.",
    (1, 7): "También Sodoma y Gomorra y las ciudades vecinas, que como ellos se entregaron a la fornicación y siguieron un uso antinatural de la carne, están puestas para escarmiento, sufriendo el castigo de un fuego eterno.",
    
    # Su conducta inmoral y escandalosa (8-13)
    (1, 8): "Su conducta inmoral y escandalosa: También éstos, a pesar de todo, en su delirio manchan su cuerpo, desprecian la autoridad del Señor y blasfeman contra los seres gloriosos.",
    (1, 9): "El arcángel Miguel, cuando —oponiéndose al diablo— disputaba sobre el cuerpo de Moisés, no se atrevió a pronunciar una sentencia injuriosa, sino que dijo: ¡Que el Señor te reprenda!",
    (1, 10): "Pero éstos blasfeman contra todo lo que desconocen; y en lo que conocen por instinto natural como las bestias irracionales, en eso se corrompen.",
    (1, 11): "¡Ay de ellos!, porque se metieron por el camino de Caín, y se precipitaron por afán de lucro en la aberración de Balaán, y perecieron en la rebelión de Coré.",
    (1, 12): "Éstos son una mancha en vuestros ágapes: comportándose sin recato como si estuvieran en banquetes, se cuidan a sí mismos; son nubes sin agua zarandeadas por los vientos; árboles de otoño sin fruto, dos veces muertos y arrancados de raíz.",
    (1, 13): "Olas bravías del mar que echan la espuma de sus torpezas; astros errantes a los que está reservada para siempre la oscuridad tenebrosa.",
    
    # El juicio de Dios (14-16)
    (1, 14): "El juicio de Dios: De ellos también profetizó Henoc, el séptimo descendiente de Adán, cuando dijo: «Mira, ha venido el Señor con sus santas miríadas.",
    (1, 15): "Para entablar juicio contra todos y dejar convictos a todos los impíos de todas las perversidades que han cometido, y de todas las injurias que los pecadores impíos han proferido contra él».",
    (1, 16): "Éstos son unos murmuradores que se quejan de su suerte, viviendo al dictado de sus concupiscencias; y su boca pronuncia palabras hinchadas, adulando a las personas por su propio interés.",
    
    # II. EXHORTACIONES A LOS FIELES - Estaba predicha la aparición de los impíos (17-19)
    (1, 17): "II. EXHORTACIONES A LOS FIELES - Estaba predicha la aparición de los impíos: Pero vosotros, queridísimos, acordaos de las palabras anunciadas por medio de los apóstoles de nuestro Señor Jesucristo.",
    (1, 18): "Que os decían: «En los últimos tiempos habrá quienes se burlen de todo y vivan según sus impías concupiscencias».",
    (1, 19): "Éstos son los que crean divisiones, hombres meramente naturales, que no tienen el Espíritu.",
    
    # Las virtudes teologales (20-21)
    (1, 20): "Las virtudes teologales: Pero vosotros, queridísimos, edificándoos sobre vuestra santísima fe y orando en el Espíritu Santo.",
    (1, 21): "Manteneos en el amor de Dios, aguardando que la misericordia de nuestro Señor Jesucristo os conceda la vida eterna.",
    
    # Comportamiento con los que vacilan (22-23)
    (1, 22): "Comportamiento con los que vacilan: Tratad con compasión a los que vacilan.",
    (1, 23): "A unos procurad salvarlos, arrancándolos del fuego; a otros tratadlos con misericordia, pero con precaución, aborreciendo hasta la túnica contaminada por su carne.",
    
    # Doxología final (24-25)
    (1, 24): "Doxología final: Al que es poderoso para guardaros sin tropiezo y presentaros sin tacha y con júbilo delante de su gloria.",
    (1, 25): "Al único Dios, Salvador nuestro por medio de Jesucristo nuestro Señor, la gloria, la majestad, el imperio y la potestad, desde siempre y ahora y por todos los siglos. Amén."
}

# Parsed comments for Philemon - each section to specific verses
philemon_comments = {
    # Saludo (1-3)
    (1, 1): "Saludo: Pablo, prisionero de Cristo Jesús, y Timoteo, el hermano, a Filemón, nuestro querido amigo y colaborador.",
    (1, 2): "A Apfia, la hermana, a Arquipo, nuestro compañero de armas, y a la iglesia que se reúne en tu casa.",
    (1, 3): "La gracia y la paz de Dios, nuestro Padre, y del Señor Jesucristo estén con vosotros.",
    
    # Acción de gracias (4-7)
    (1, 4): "Acción de gracias: Doy gracias sin cesar a mi Dios recordándote en mis oraciones.",
    (1, 5): "Porque conozco la caridad y la fe que tienes en Jesús, el Señor, y en todos los santos.",
    (1, 6): "Que tu participación en la misma fe llegue a ser activa al comprender que todo el bien que tenemos es para Cristo.",
    (1, 7): "Pues, en verdad, he tenido gran alegría y consuelo por tu caridad, porque, gracias a ti, hermano, los corazones de los santos han encontrado alivio.",
    
    # Intercesión en favor de Onésimo (8-13)
    (1, 8): "Intercesión en favor de Onésimo: Aun teniendo plena libertad en Cristo para mandarte lo que conviene.",
    (1, 9): "Prefiero rogar en nombre de la caridad —y eso que soy Pablo, ya anciano y ahora además prisionero de Cristo Jesús—.",
    (1, 10): "Te ruego en favor de mi hijo Onésimo, a quien engendré entre cadenas.",
    (1, 11): "En otro tiempo inútil para ti pero ahora útil para ti y para mí.",
    (1, 12): "A éste te lo devuelvo como si fuera mi corazón.",
    (1, 13): "Yo hubiera querido retenerlo para que me sirviera en tu lugar, mientras estoy entre cadenas por el Evangelio.",
    
    # Continuación (14-16)
    (1, 14): "Pero no he querido hacer nada sin tu consentimiento, para que tu buena acción no sea forzada, sino voluntaria.",
    (1, 15): "Quizá por eso se alejó algún tiempo, para que ahora lo recuperes para siempre.",
    (1, 16): "No ya como siervo, sino más que siervo, como hermano muy amado, en primer lugar para mí, pero ¡cuánto más para ti!, no sólo en lo humano, sino también en el Señor.",
    
    # Petición final (17-21)
    (1, 17): "Por tanto, si me consideras hermano en la fe, acógelo como si fuera yo mismo.",
    (1, 18): "Si te perjudicó o te debe algo, cárgalo a mi cuenta.",
    (1, 19): "Yo, Pablo, lo he escrito de mi puño y letra; yo te pagaré, por no decirte que tú mismo te me debes.",
    (1, 20): "Sí, hermano, que yo reciba de ti este gozo en el Señor. Consuela en Cristo mi corazón.",
    (1, 21): "Te escribo confiando en tu obediencia, porque sé que harás aun más de lo que te digo.",
    
    # Últimas recomendaciones y saludos (22-25)
    (1, 22): "Últimas recomendaciones y saludos: Además, prepárame hospedaje, pues espero que, gracias a vuestras oraciones, se me conceda estar entre vosotros.",
    (1, 23): "Te saludan Epafras, compañero de mi cautiverio en Cristo Jesús.",
    (1, 24): "Y mis colaboradores Marcos, Aristarco, Demas y Lucas.",
    (1, 25): "La gracia del Señor Jesucristo esté con vuestro espíritu."
}

print("Fixing Jude and Philemon comments with proper verse-specific assignments...")

# Decompress
gz_path = "public/bibles/navarra.sqlite.gz"
db_path = "scripts/temp_fix_jude_phm.sqlite"

with gzip.open(gz_path, 'rb') as f_in:
    with open(db_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Update Jude with verse-specific comments
jude_updated = 0
for (ch, v), comment in jude_comments.items():
    cursor.execute(
        "UPDATE verses SET comment = ? WHERE book = 'JUD' AND chapter = ? AND verse = ?",
        (comment, ch, v)
    )
    if cursor.rowcount > 0:
        jude_updated += 1

print(f"Updated {jude_updated} verses in Jude with specific comments")

# Update Philemon with verse-specific comments
phm_updated = 0
for (ch, v), comment in philemon_comments.items():
    cursor.execute(
        "UPDATE verses SET comment = ? WHERE book = 'PHM' AND chapter = ? AND verse = ?",
        (comment, ch, v)
    )
    if cursor.rowcount > 0:
        phm_updated += 1

print(f"Updated {phm_updated} verses in Philemon with specific comments")

# Verify
cursor.execute("SELECT COUNT(*) FROM verses WHERE book = 'JUD' AND comment IS NOT NULL AND comment != ''")
jude_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM verses WHERE book = 'PHM' AND comment IS NOT NULL AND comment != ''")
phm_count = cursor.fetchone()[0]

print(f"\nVerification:")
print(f"JUD: {jude_count}/25 verses now have specific comments")
print(f"PHM: {phm_count}/25 verses now have specific comments")

# Sample
print("\nSample comments:")
cursor.execute("SELECT verse, comment FROM verses WHERE book = 'JUD' ORDER BY verse LIMIT 3")
for r in cursor.fetchall():
    print(f"  Jude 1:{r[0]} - {r[1][:80]}...")

cursor.execute("SELECT verse, comment FROM verses WHERE book = 'PHM' ORDER BY verse LIMIT 3")
for r in cursor.fetchall():
    print(f"  Philemon 1:{r[0]} - {r[1][:80]}...")

conn.commit()
conn.close()

# Recompress
print("\nRecompressing database...")
with open(db_path, 'rb') as f_in:
    with gzip.open(gz_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

os.remove(db_path)
print("Done!")
