import sqlite3
import gzip
import shutil
import os

# Decompress database
gz_path = 'public/bibles/navarra.sqlite.gz'
db_path = 'scripts/temp_jude_phm.sqlite'

print('Decompressing database...')
with gzip.open(gz_path, 'rb') as f_in:
    with open(db_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Clear existing comments
print('Clearing existing comments from Jude and Philemon...')
cursor.execute('UPDATE verses SET comment = NULL WHERE book = ?', ('JUD',))
cursor.execute('UPDATE verses SET comment = NULL WHERE book = ?', ('PHM',))
conn.commit()

# PHILEMON COMMENTS
print('Adding Philemon comments...')

# Flm 1-3
phm_1_3 = '''La brevedad de esta carta ayuda a percibir mejor el esquema que seguía San Pablo en su correspondencia: saludos; acción de gracias a Dios u oración; contenido que quiere transmitir; y despedida final. Además, esta carta es de gran interés para valorar y orientar cristianamente las condiciones sociales en que viven los cristianos. Es posible que Apfia y Arquipo sean miembros de la familia de Filemón, quizá su esposa e hijo. Arquipo tenía un puesto importante en la iglesia de Colosas (cfr Col 4,17). San Jerónimo hace notar que «Pablo no usa la expresión "prisionero de Cristo Jesús" en ninguna otra carta, aunque esté claro que se encuentra en la cárcel por su fe, según el contenido de las cartas a los efesios, filipenses y colosenses. Me parece —añade— que es un mayor orgullo el que diga que está prisionero por Cristo, que el ser apóstol. Ellos salían gozosos de la presencia del Sanedrín, porque habían sido dignos de ser ultrajados a causa del Nombre (Hch 5,41). La autoridad de su encarcelamiento hace que, al interceder por Onésimo, sea tal la fuerza de su ruego que consiga lo que pide» (S. Jerónimo, Commentarii in Philemonem, ad loc.).'''

for v in [1, 2, 3]:
    cursor.execute('UPDATE verses SET comment = ? WHERE book = ? AND chapter = 1 AND verse = ?',
                   (phm_1_3, 'PHM', v))

# Flm 4-7
phm_4_7 = '''El v. 5 sintetiza una enseñanza de gran importancia teológica. Pablo enseña que un cristiano no sólo ha de amar y tener fe en Cristo, sino por Él y en Él, amar y tener fe en los demás cristianos. Filemón y Onésimo deben fiarse uno del otro porque ambos son hermanos en Cristo. Esta misma argumentación vuelve a aparecer en el v. 16, y está también presente en vv. 17-21. El v. 6 tiene una redacción oscura. Quiere decir que al participar de la misma fe, los cristianos alcanzan la comunión con Cristo y con los demás creyentes. Además, Pablo confía en que la fe de Filemón llegue a ser una fe práctica, operativa, con la profunda comprensión de que todos los bienes que hemos alcanzado los cristianos tienen una estrecha relación con Cristo. Gramaticalmente esa relación con Cristo está expresada de manera tan concisa, «para Cristo», que puede entenderse como «para gloria de Cristo» o «por medio de Cristo». «Era razonable que el maestro mandase al discípulo usando de su autoridad apostólica. Pero como Filemón era un buen cristiano, [el Apóstol], como anciano y como prisionero por Cristo, apela al amor para provocar la obediencia» (Ambrosiaster, Ad Philemonem).'''

for v in [4, 5, 6, 7]:
    cursor.execute('UPDATE verses SET comment = ? WHERE book = ? AND chapter = 1 AND verse = ?',
                   (phm_4_7, 'PHM', v))

# Flm 8-21 (first part)
phm_8_21 = '''San Pablo ha engendrado a la fe a Onésimo, esclavo fugitivo de Filemón. El Apóstol juega con el significado de la palabra Onésimo (= útil), para interceder por él ante su antiguo amo y pedirle a Filemón que lo reciba de nuevo. Conviene reparar en el hecho de que el Apóstol llevó el mensaje del Evangelio a todos, sin distinción de clases ni condiciones sociales, es más, manifestando especial afecto a los más desfavorecidos, a los que no contempla —según era frecuente en la época— como inferiores, sino como hermanos muy amados. «Ved a Pablo escribiendo a favor de Onésimo, un esclavo fugitivo —comenta San Juan Crisóstomo—; no se avergüenza de llamarlo hijo suyo, sus propias entrañas, su hermano, su bienamado» (In Philemonem 2, ad loc.). Y es que un cristiano está llamado a estimar a todos los hombres como hermanos, valorando la dignidad de la persona humana, y consiguientemente sus derechos. Nadie puede sentirse ajeno a esa actitud ni dejar de asumir los propios deberes, con una inhibición que constituiría un pecado social, que ofende a Dios y a la sociedad de los hombres. Así lo expresa con claridad Juan Pablo II: «Es social todo pecado cometido contra la justicia en las relaciones tanto interpersonales como en las de la persona con la sociedad, y aun de la comunidad con la persona. Es social todo pecado cometido contra los derechos de la persona humana, comenzando por el derecho a la vida, sin excluir la del que está por nacer, o contra la integridad física de alguno; todo pecado contra la libertad ajena, especialmente contra la suprema libertad de creer en Dios y de adorarlo; todo pecado contra la dignidad y el honor del prójimo. Es social todo pecado contra el bien común y sus exigencias, dentro del amplio panorama de los derechos y deberes de los ciudadanos. Puede ser social el pecado de obra u omisión por parte de dirigentes políticos, económicos y sindicales, que aun pudiéndolo, no se empeñan con sabiduría en el mejoramiento o en la transformación de la sociedad según las exigencias y las posibilidades del momento histórico; así como por parte de trabajadores que no cumplen con sus deberes de presencia y colaboración, para que las fábricas puedan seguir dando bienestar a ellos mismos, a sus familias y a toda la sociedad» (Reconciliatio et paenitentia, n. 16).'''

for v in range(8, 21):
    cursor.execute('UPDATE verses SET comment = ? WHERE book = ? AND chapter = 1 AND verse = ?',
                   (phm_8_21, 'PHM', v))

# Flm 21 (additional)
phm_21_extra = '''San Pablo no afronta directamente el tema de la esclavitud, que pertenecía a la estructura social de la época, pero aporta los principios cristianos que son el germen de la abolición de la esclavitud en los lugares donde el espíritu cristiano ha impregnado las conciencias de los ciudadanos y las leyes de los pueblos. Sin embargo, el Apóstol reclama delicadamente una conducta coherente con la doctrina del Evangelio. Éste es el contenido de ese «más» que Pablo esperaba de Filemón: debía tratar a Onésimo como verdadero hermano en la fe, en plano de igualdad, sin acepción alguna por motivo de clase o condición. «Convenceos de que únicamente con la justicia no resolveréis nunca los grandes problemas de la humanidad. Cuando se hace justicia a secas, no os extrañéis si la gente se queda herida: pide mucho más la dignidad del hombre, que es hijo de Dios. La caridad ha de ir dentro y al lado, porque lo dulcifica todo, lo deifica: 'Dios es amor' (1 Jn 4,16). Hemos de movernos siempre por Amor de Dios, que torna más fácil querer al prójimo, y purifica y eleva los amores terrenos» (S. Josemaría Escrivá, Amigos de Dios, n. 172).'''

cursor.execute('UPDATE verses SET comment = ? WHERE book = ? AND chapter = 1 AND verse = 21',
               (phm_8_21 + '<br><br>' + phm_21_extra, 'PHM'))

# Flm 22-25
phm_22_25 = '''Junto con los saludos de quienes acompañan en ese momento a San Pablo, mencionados en Col 4,10-14, aparece la bendición final acostumbrada. Se aprecia la importancia que debía tener para aquella naciente cristiandad de Colosas la familia y la casa de Filemón. Es un ejemplo más del papel que jugaron las familias cristianas en la difusión del Evangelio (cfr nota a Rm 16,1-23).'''

for v in [22, 23, 24, 25]:
    cursor.execute('UPDATE verses SET comment = ? WHERE book = ? AND chapter = 1 AND verse = ?',
                   (phm_22_25, 'PHM', v))

# JUDE COMMENTS
print('Adding Jude comments...')

# Jds 1-2
jud_1_2 = '''En esta carta encontramos, en forma más breve, temas similares a los de la Segunda Carta de San Pedro. El autor, tras exponer el motivo por el que se ve obligado a escribir (vv. 3-4), recuerda cómo Dios castigó a aquellos hombres cuya conducta blasfema y licenciosa están imitando ahora algunos (vv. 5-16). En contraposición, anima a los fieles a mantenerse firmes en la fe y en la caridad (vv. 17-23). Concluye con una solemne alabanza a Dios por Cristo (vv. 24-25). Con las expresiones con que designa a sus destinatarios (v. 1), el autor describe lo que es un cristiano: su vida se inicia con la llamada divina, progresa gracias al amor de Dios y culmina en Jesucristo. «Los que han recibido la llamada divina» (v. 1). Literalmente, «los llamados» (cfr Rm 1,6; 1 Co 1,24). A la misma raíz griega pertenece también la palabra «Iglesia», que es la comunidad de aquellos que Dios «llamó de las tinieblas a su admirable luz» (1 P 2,9), el nuevo pueblo de Dios, elegido por Él libre y gratuitamente.'''

for v in [1, 2]:
    cursor.execute('UPDATE verses SET comment = ? WHERE book = ? AND chapter = 1 AND verse = ?',
                   (jud_1_2, 'JUD', v))

# Jds 3-4
jud_3_4 = '''Estos versículos manifiestan el motivo de la carta y el propósito de su autor. La fe «entregada a los santos» supone un depósito de verdades ya formado, que el autor sagrado quiere defender (cfr p. ej. Ga 1,6-9; 1 Co 11,23ss.; 15,1ss.). Ahora es la Iglesia quien continúa la tarea: «Ella es la que guarda la memoria de las Palabras de Cristo, la que transmite de generación en generación la confesión de fe de los Apóstoles. Como una madre que enseña a sus hijos a hablar y con ello a comprender y a comunicar, la Iglesia, nuestra Madre, nos enseña el lenguaje de la fe para introducirnos en la inteligencia y la vida de la fe» (Catecismo de la Iglesia Católica, n. 171). «Se han infiltrado» (v. 4). El término griego, que significa «entrar desde fuera», expresa bien el proceder de los falsos maestros; probablemente eran predicadores itinerantes, que iban de una comunidad a otra. Se señala un doble error: uno de orden práctico y moral, pues convierten la gracia en libertinaje; y otro de orden doctrinal, porque niegan a Jesucristo. Con el pretexto de la libertad ganada por Cristo, rebajaban las exigencias de la lucha contra el pecado. Por el contrario, la realidad es que, para profundizar en el verdadero alcance de la libertad, hay que mirar a Jesucristo. «La libertad adquiere su auténtico sentido cuando se ejercita en servicio de la verdad que rescata, cuando se gasta en buscar el Amor infinito de Dios, que nos desata de todas las servidumbres» (S. Josemaría Escrivá, Amigos de Dios, n. 27).'''

for v in [3, 4]:
    cursor.execute('UPDATE verses SET comment = ? WHERE book = ? AND chapter = 1 AND verse = ?',
                   (jud_3_4, 'JUD', v))

# Jds 5-16 general intro
jud_5_16_intro = '''Esta sección de la carta desenmascara a los «impíos» anunciando el fin que les espera.'''

# Jds 5-7
jud_5_7 = '''Los tres ejemplos bíblicos parecen señalar tres vicios fundamentales (cfr v. 8): los israelitas incrédulos y murmuradores que perecieron en el desierto (Nm 14) son paradigma de incredulidad; los ángeles que, rebelándose contra Dios, pecaron con mujeres, para ser, según la tradición judía, aherrojados en el infierno por Dios (Gn 6,1-2; Libro de Henoc 10,4-6; caps. 12 y 13), son manifestación de desobediencia y soberbia; las perversiones de Sodoma y Gomorra (Gn 18,16ss.) son prototipo de impureza. Ver también 2 P 2,4-10. El v. 7 es una condena explícita de la homosexualidad (cfr Rm 1,24-27; 1 Co 6,9; 1 Tm 1,10). Apoyándose en estos y otros textos de la Escritura, «la Tradición ha declarado siempre que "los actos homosexuales son intrínsecamente desordenados" (Cong. Doctrina de la Fe, Persona humana, n. 8). Son contrarios a la ley natural. Cierran el acto sexual al don de la vida. No proceden de una complementariedad afectiva y sexual verdadera. No pueden recibir aprobación en ningún caso» (Catecismo de la Iglesia Católica, n. 2357). cfr nota a Rm 1,18-32. «El Señor» (v. 5). En otros manuscritos griegos se lee «Jesús», atribuyendo así más expresamente la liberación del pueblo de Israel de la tierra de Egipto a Cristo, e interpretando así el Antiguo Testamento a la luz del Nuevo, que es su plenitud. «El castigo de un fuego eterno» (v. 7) manifiesta el carácter irrevocable del juicio divino. La fe de la Iglesia se ha hecho eco de esta expresión al ilustrar las penas que los condenados sufren en el infierno (cfr nota a Ap 20,7-10). Sin embargo, la existencia del infierno, y de los otros «novísimos», es doctrina cristiana, revelada no para provocar terror, sino para estimular a la conversión y a la perseverancia en el bien: «Solamente en esa visión escatológica se puede tener la medida exacta del pecado y sentirse impulsados decididamente a la penitencia y a la reconciliación» (Juan Pablo II, Reconciliatio et paenitentia, n. 26).'''

for v in [5, 6, 7]:
    cursor.execute('UPDATE verses SET comment = ? WHERE book = ? AND chapter = 1 AND verse = ?',
                   (jud_5_16_intro + '<br><br>' + jud_5_7, 'JUD', v))

# Jds 8-13
jud_8_13 = '''Para ilustrar mejor la maldad del comportamiento de los «intrusos» (cfr v. 4), el autor sagrado acude (vv. 9-10) a la leyenda popular recogida en el apócrifo La Asunción de Moisés, según la cual, cuando San Miguel iba a enterrar el cuerpo de Moisés, el diablo intentó arrebatárselo. San Miguel se lo impidió pero no injurió al diablo, sólo apeló al juicio de Dios. Ver también nota a 2 P 2,10-19. Con otros tres ejemplos bíblicos (vv. 11-13) destaca la conducta perversa de los falsarios: Caín (Gn 4,3; cfr 1 Jn 3,12), Balaán (Nm 31,16; Ap 2,14; cfr 2 P 2,15), Coré y sus seguidores que se rebelaron contra Moisés (Nm 16). Los falsos maestros no tienen inconveniente en asistir a celebraciones de los cristianos, pero llevan una vida amoral. Participan en las comidas fraternas —ágapes— de los cristianos (cfr nota a 1 Co 11,17-22), donde dan rienda suelta a su gula y propagan sus errores. Son así una «mancha» (v. 12). El término griego traducido de esta manera equivale a escándalo. Originariamente significa «escollo», es decir, una roca que está a flor de agua y es por tanto peligrosa para la navegación, pero también puede traducirse por «mancha», en sentido propio o moral, como hace la Neovulgata. Comenta San Beda: «Manchado está el que peca. El pecado mismo es una mancha que contamina a quien peca» (In Epistolam Iudae, ad loc.). Son «nubes sin agua», porque «no tienen en sí la fecundidad de la palabra divina» (Clemente de Alejandría, Exegesis in Iudam, ad loc.). «Dos veces muertos» (v. 12). Quizá se refiere a que su apartamiento de la fe es peor que el estado anterior al Bautismo (cfr 2 P 2,20-22).'''

for v in range(8, 14):
    cursor.execute('UPDATE verses SET comment = ? WHERE book = ? AND chapter = 1 AND verse = ?',
                   (jud_5_16_intro + '<br><br>' + jud_8_13, 'JUD', v))

# Jds 14-16
jud_14_16 = '''Se cita ahora expresamente el Libro de Henoc, apócrifo escrito años antes de Jesucristo, que recoge muchos relatos legendarios sobre textos oscuros del Antiguo Testamento. Henoc era una figura misteriosa de gran prestigio en la tradición judía. Caminó en la presencia de Dios y fue llevado al cielo antes de morir. Fue alabado por su bondad (cfr Gn 5,6.22-24; cfr Si 44,16; 49,14; Hb 11,5). Hay otras alusiones al Libro de Henoc a lo largo de la carta (vv. 6-7). En el lenguaje apocalíptico de esta clase de literatura se habla de acontecimientos futuros como si ya hubiesen sucedido. San Judas se sirve de él para ilustrar la doctrina sobre el castigo de los «impíos».'''

for v in [14, 15, 16]:
    cursor.execute('UPDATE verses SET comment = ? WHERE book = ? AND chapter = 1 AND verse = ?',
                   (jud_5_16_intro + '<br><br>' + jud_14_16, 'JUD', v))

# Jds 17-25 general intro
jud_17_25_intro = '''Ante los errores de los falsos maestros, esta sección de la carta exhorta a custodiar la fe, a la práctica de las virtudes y al buen ejemplo.'''

# Jds 17-19
jud_17_19 = '''Estos avisos se remontan en última instancia a lo que Cristo había predicho: «Surgirán falsos mesías y falsos profetas, y se presentarán con grandes señales y prodigios para engañar, si fuera posible, incluso a los elegidos» (Mt 24,24). Los «últimos tiempos» (v. 18) es una expresión que hace referencia a la era mesiánica, que ha comenzado con la venida de Cristo (cfr Ga 4,4). «Hombres meramente naturales» (v. 19). Literalmente sería «hombres psíquicos». Como en algunos textos de San Pablo (cfr 1 Co 2,14; 15,44-46), éstos se oponen a los hombres «espirituales», es decir, a los cristianos que poseen el Espíritu Santo, y le son dóciles (cfr Rm 5,5; 8,14). En cambio, quienes «no tienen el Espíritu», que es el principio de la vida sobrenatural, juzgan y viven guiados únicamente por la naturaleza humana herida por el pecado original. Su sabiduría es meramente terrena (cfr St 3,15), carnal (cfr 1 Co 3,3). Son los que crean divisiones entre los creyentes: «No será partícipe de la divina caridad quien es enemigo de la unidad. Y así no tienen el Espíritu Santo los que están fuera de la Iglesia» (S. Agustín, Epistolae 185,11,50).'''

for v in [17, 18, 19]:
    cursor.execute('UPDATE verses SET comment = ? WHERE book = ? AND chapter = 1 AND verse = ?',
                   (jud_17_25_intro + '<br><br>' + jud_17_19, 'JUD', v))

# Jds 20-21
jud_20_21 = '''Como en otros lugares del Nuevo Testamento, la invocación a las tres Personas divinas viene acompañada de una exhortación a las tres virtudes teologales: «Las virtudes teologales se refieren directamente a Dios. Disponen a los cristianos a vivir en relación con la Santísima Trinidad. Tienen como origen, motivo y objeto a Dios Uno y Trino» (Catecismo de la Iglesia Católica, n. 1812).'''

for v in [20, 21]:
    cursor.execute('UPDATE verses SET comment = ? WHERE book = ? AND chapter = 1 AND verse = ?',
                   (jud_17_25_intro + '<br><br>' + jud_20_21, 'JUD', v))

# Jds 22-23
jud_22_23 = '''Los cristianos han de tratar siempre con misericordia a los que se apartan de la buena doctrina, a la vez que evitan el peligro para sus almas. «Es propio de los perfectos que en los pecadores no odien más que los pecados; y que amen a esos mismos hombres» (S. Agustín, Contra Adimantum 17,5).'''

for v in [22, 23]:
    cursor.execute('UPDATE verses SET comment = ? WHERE book = ? AND chapter = 1 AND verse = ?',
                   (jud_17_25_intro + '<br><br>' + jud_22_23, 'JUD', v))

#Jds 24-25
jud_24_25 = '''La doxología o alabanza a Dios Padre por medio de Jesucristo enseña que Jesús es el Mediador tanto de nuestra salvación como de nuestra alabanza al Padre. Desde sus inicios, la Iglesia tiene la costumbre de dirigir la oración litúrgica al Padre por medio de Jesucristo. San Beda, comentando el v. 25, escribe: «Este versículo asigna al Padre y al Hijo igual y coeterna gloria y poder por los siglos de los siglos. Y acusa de estar en el error a quienes creen que el Hijo es inferior y posterior que el Padre, pues dice que la gloria, la majestad, el imperio y la potestad son para el Padre por medio de Jesucristo, nuestro Señor. Y esto no empezó en algún momento, sino desde antes de los siglos, y ahora, por todos los siglos. Amén» (In Epistolam Iudae, ad loc.).'''

for v in [24, 25]:
    cursor.execute('UPDATE verses SET comment = ? WHERE book = ? AND chapter = 1 AND verse = ?',
                   (jud_17_25_intro + '<br><br>' + jud_24_25, 'JUD', v))

# Commit changes
conn.commit()

# Verify
cursor.execute('SELECT COUNT(*) FROM verses WHERE book = ? AND comment IS NOT NULL', ('JUD',))
jud_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM verses WHERE book = ? AND comment IS NOT NULL', ('PHM',))
phm_count = cursor.fetchone()[0]

print(f'\nVerification:')
print(f'Jude: {jud_count}/25 verses have comments')
print(f'Philemon: {phm_count}/25 verses have comments')

# Sample
print('\nSample Jude comments:')
cursor.execute('SELECT verse, comment FROM verses WHERE book = ? ORDER BY verse LIMIT 3', ('JUD',))
for row in cursor.fetchall():
    print(f'  Jude 1:{row[0]} - {row[1][:80]}...')

print('\nSample Philemon comments:')
cursor.execute('SELECT verse, comment FROM verses WHERE book = ? ORDER BY verse LIMIT 3', ('PHM',))
for row in cursor.fetchall():
    print(f'  Philemon 1:{row[0]} - {row[1][:80]}...')

conn.close()

# Recompress
print('\nRecompressing database...')
with open(db_path, 'rb') as f_in:
    with gzip.open(gz_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

os.remove(db_path)
print('Done!')
