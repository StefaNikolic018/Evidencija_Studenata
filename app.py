from flask import Flask, render_template, url_for, request, redirect, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

konekcija = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    passwd='',
    database='pajtonsajt'
)

kursor = konekcija.cursor(dictionary=True)


def ulogovan():
    if 'ulogovani_korisnik' in session:
        return True
    else:
        return False


app = Flask(__name__)

app.secret_key = 'nasTajniKljuc'


@app.route('/')
def index():
    if ulogovan():
        return redner_template('studenti.html')
    else:
        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    poruka = None
    if request.method == 'GET':
        return render_template('login.html', poruka=poruka)
    elif request.method == 'POST':
        forma = request.form
        if forma['email'] == '' or forma['lozinka'] == '':
            poruka = 'Niste popunili sva polja !'
            return render_template('login.html', poruka=poruka)
        else:
            upit = "SELECT * FROM korisnici WHERE email=%s"
            vrednost = (forma['email'],)
            kursor.execute(upit, vrednost)
            korisnik = kursor.fetchone()
            if check_password_hash(korisnik['lozinka'], forma['lozinka']):
                session['ulogovani_korisnik'] = str(korisnik)
                flash('Dobrodošli ' +
                      str(korisnik['ime'] + '!'), 'dobrodoslica')
                return redirect(url_for('studenti'))
            else:
                poruka = 'Pogrešili ste lozinku !'
                return render_template('login.html', poruka=poruka)


@app.route('/logout')
def logout():
    session.pop('ulogovani_korisnik', None)
    flash('Uspešno ste izlogovani!', 'uspeh')
    return redirect(url_for('login'))


@app.route('/studenti')
def studenti():
    if ulogovan():
        upit = "SELECT * FROM studenti"
        kursor.execute(upit)
        studenti = kursor.fetchall()
        return render_template('studenti.html', studenti=studenti)
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


@app.route('/korisnici')
def korisnici():
    if ulogovan():
        upit = "SELECT * FROM korisnici "
        kursor.execute(upit)
        korisnici = kursor.fetchall()
        return render_template('korisnici.html', korisnici=korisnici)
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


@app.route('/predmeti')
def predmeti():
    if ulogovan():
        upit = "SELECT * FROM predmeti"
        kursor.execute(upit)
        predmeti = kursor.fetchall()
        return render_template('predmeti.html', predmeti=predmeti)
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


@app.route('/student_novi', methods=['GET', 'POST'])
def student_novi():
    if ulogovan():
        if request.method == 'GET':
            return render_template('student_novi.html')
        elif request.method == 'POST':
            forma = request.form
            upit = """ INSERT INTO
						studenti (ime,ime_roditelja,prezime,broj_indeksa,godina_studija,
						          jmbg,datum_rodjenja,broj_telefona,email,espb,prosek_ocena)
						VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s,%s,%s)"""
            vrednosti = (forma['ime'], forma['ime_roditelja'], forma['prezime'], forma['broj_indeksa'], forma['godina_studija'],
                         forma['jmbg'], forma['datum_rodjenja'], forma['broj_telefona'], forma['email'], '0', '0')
            kursor.execute(upit, vrednosti)
            konekcija.commit()
            flash('Uspešno ste dodali studenta !', 'stud')
            return redirect(url_for('studenti'))
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


@app.route('/korisnik_novi', methods=['GET', 'POST'])
def korisnik_novi():
    if ulogovan():
        if request.method == 'GET':
            return render_template('korisnik_novi.html')
        elif request.method == 'POST':
            forma = request.form
            upit = """ INSERT INTO
						korisnici (ime,prezime,email,lozinka)
						VALUES (%s, %s, %s, %s) """
            hesovana_lozinka = generate_password_hash(forma['lozinka'])
            vrednosti = (forma['ime'], forma['prezime'],
                         forma['email'], hesovana_lozinka)
            kursor.execute(upit, vrednosti)
            konekcija.commit()
            flash('Uspešno ste dodali korisnika !', 'koris')
            return redirect(url_for('korisnici'))
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


@app.route('/predmet_novi', methods=['GET', 'POST'])
def predmet_novi():
    if ulogovan():
        if request.method == 'GET':
            return render_template('predmet_novi.html')
        elif request.method == 'POST':
            forma = request.form
            upit = """ INSERT INTO
						predmeti (sifra, naziv, godina_studija, espb, obavezni_izborni)
						VALUES (%s,%s,%s,%s,%s)
					"""
            vrednosti = (forma['sifra'], forma['naziv'], forma['godina_studija'],
                         forma['espb'], forma['obavezni_izborni'])
            kursor.execute(upit, vrednosti)
            konekcija.commit()
            flash('Uspešno ste dodali predmet !', 'pred')
            return redirect(url_for('predmeti'))
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


@app.route('/student_izmena/<id>', methods=['GET', 'POST'])
def student_izmena(id):
    if ulogovan():
        if request.method == 'GET':
            upit = "SELECT * FROM studenti WHERE id=%s"
            vrednost = (id,)
            kursor.execute(upit, vrednost)
            student = kursor.fetchone()
            return render_template('student_izmena.html', student=student)
        elif request.method == 'POST':
            upit1="SELECT espb FROM studenti WHERE id=%s"
            vr=(id,)
            kursor.execute(upit1, vr)
            espb=kursor.fetchone()
            upit2="SELECT prosek_ocena FROM studenti WHERE id=%s"
            vr1=(id,)
            kursor.execute(upit2,vr1)
            prosek_ocena=kursor.fetchone()
            upit = """UPDATE studenti
						SET ime=%s,ime_roditelja=%s,prezime=%s,broj_indeksa=%s,godina_studija=%s,jmbg=%s,datum_rodjenja=%s,espb=%s,prosek_ocena=%s,broj_telefona=%s,email=%s
						WHERE id=%s
						"""
            forma = request.form
            vrednosti = (forma['ime'], forma['ime_roditelja'], forma['prezime'], forma['broj_indeksa'], forma['godina_studija'],
                         forma['jmbg'], forma['datum_rodjenja'], str(espb['espb']), str(prosek_ocena['prosek_ocena']), forma['broj_telefona'], forma['email'], id)
            kursor.execute(upit, vrednosti)
            konekcija.commit()
            flash('Uspešno ste izmenili informacije studenta!','stud')
            return redirect(url_for('studenti'))
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


@app.route('/korisnik_izmena/<id>', methods=['GET', 'POST'])
def korisnik_izmena(id):
    if ulogovan():
        if request.method == 'GET':
            upit = "SELECT * FROM korisnici WHERE id=%s"  # string
            vrednost = (id,)  # tuple
            kursor.execute(upit, vrednost)
            korisnik = kursor.fetchone()
            return render_template('korisnik_izmena.html', korisnik=korisnik)
        elif request.method == 'POST':
            upit = """ UPDATE korisnici
						SET ime=%s, prezime=%s, email=%s, lozinka=%s
						WHERE id=%s
					"""
            forma = request.form
            vrednosti = (forma['ime'], forma['prezime'],
                         forma['email'], forma['lozinka'], id)
            kursor.execute(upit, vrednosti)
            konekcija.commit()
            flash('Uspešno ste izmenili informacije korisnika!', 'koris')
            return redirect(url_for('korisnici'))
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


@app.route('/predmet_izmena/<id>', methods=['GET', 'POST'])
def predmet_izmena(id):
    if ulogovan():
        if request.method == 'GET':
            upit = "SELECT * FROM predmeti WHERE id=%s"
            vrednost = (id,)
            kursor.execute(upit, vrednost)
            predmet = kursor.fetchone()
            return render_template('predmet_izmena.html', predmet=predmet)
        elif request.method == 'POST':
            forma = request.form
            upit = """UPDATE predmeti
						SET sifra=%s, naziv=%s, godina_studija=%s, espb=%s,obavezni_izborni=%s
						WHERE id=%s
					"""
            vrednosti = (forma['sifra'], forma['naziv'], forma['godina_studija'],
                         forma['espb'], forma['obavezni_izborni'], id)
            kursor.execute(upit, vrednosti)
            konekcija.commit()
            flash('Uspešno ste izmenili informacije predmeta!', 'pred')
            return redirect(url_for('predmeti'))
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


@app.route('/korisnik_brisanje/<id>', methods=['POST'])
def korisnik_brisanje(id):
    if ulogovan():

        upit = "DELETE FROM korisnici WHERE id=%s"
        vrednost = (id,)
        kursor.execute(upit, vrednost)
        konekcija.commit()
        flash('Uspešno obrisan korisnik !', 'koris')
        return redirect(url_for('korisnici'))
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


@app.route('/student_brisanje/<id>', methods=['POST'])
def student_brisanje(id):
    if ulogovan():
        upit = "DELETE FROM studenti WHERE id=%s"
        vrednost = (id,)
        kursor.execute(upit, vrednost)
        konekcija.commit()
        upit1 = "DELETE * FROM ocene WHERE student_id=%s"
        vr=(id,)
        konekcija.commit()
        flash('Uspešno obrisan student !', 'bris')
        return redirect(url_for('studenti'))
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


@app.route('/predmet_brisanje/<id>', methods=['POST'])
def predmet_brisanje(id):
    if ulogovan():
        upit = "DELETE FROM predmeti WHERE id=%s"
        vrednost = (id,)
        kursor.execute(upit, vrednost)
        konekcija.commit()
        flash('Uspešno obrisan predmet !', 'pred')
        return redirect(url_for('predmeti'))
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


@app.route('/studentt/<id>', methods=['GET', 'POST'])
def studentt(id):
    if ulogovan():
        upit = "SELECT * FROM studenti WHERE id=%s"  # string
        vrednost = (id,)  # tuple
        kursor.execute(upit, vrednost)
        student = kursor.fetchone()
        upit1 = "SELECT * FROM predmeti"
        kursor.execute(upit1)
        predmeti = kursor.fetchall()
        upit2 = "SELECT * FROM ocene"
        kursor.execute(upit2)
        ocene = kursor.fetchall()
        return render_template('studentt.html', student=student, predmeti=predmeti, ocene=ocene)
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


@app.route('/dodaj_ocenu/<id>', methods=['POST'])
def dodaj_ocenu(id):
    if ulogovan():
                # unos u tabelu ocene
        forma = request.form
        upit = """
        		INSERT INTO ocene(student_id, predmet_id, datum, ocena)
        		VALUES (%s, %s, %s, %s)
    			"""
        vrednosti = (id, forma['izbor'], forma['datum'], forma['ocena'])
        kursor.execute(upit, vrednosti)
        konekcija.commit()
        # resavanje espb
        # prvo trazim stari espb
        upit = "SELECT espb FROM studenti WHERE id=%s"
        vrednosti = (id,)
        kursor.execute(upit, vrednosti)
        stari_espb = kursor.fetchone()
        # trazim espb za odabrani predmet
        upit = "SELECT espb FROM predmeti WHERE id=%s"
        vrednosti = (forma['izbor'],)
        kursor.execute(upit, vrednosti)
        predmet_espb = kursor.fetchone()
        # dobijanje novog espb
        if int(forma['ocena']) < 6:
            novi_espb = stari_espb['espb']
        else:
            novi_espb = int(stari_espb['espb'])+int(predmet_espb['espb'])
            # resavanje prosecne ocene
            # napomena: vec smo uneli novu ocenu u bazu
        upit = "SELECT AVG(ocena) FROM ocene WHERE student_id=%s AND ocena>5"
        vrednosti = (id,)
        kursor.execute(upit, vrednosti)
        novi_prosek = kursor.fetchone()
        # unos novih u bazu
        upit1 = "UPDATE studenti SET espb=%s, prosek_ocena=%s WHERE id=%s"
        vrednosti = (str(novi_espb), str(novi_prosek['AVG(ocena)']), id)
        kursor.execute(upit1, vrednosti)
        konekcija.commit()
        flash('Uspešno ste dodali ocenu !', 'ocena')
        return redirect(url_for('studentt', id=id))
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


@app.route('/ocena_brisanje/<id>/<id1>', methods=['POST'])
def ocena_brisanje(id, id1):
    if ulogovan():
                # nalazim id predmeta
        upit = "SELECT predmet_id FROM ocene WHERE id=%s"
        vrednost = (id,)
        kursor.execute(upit, vrednost)
        predmet_id = kursor.fetchone()
        # nalazim espb predmeta
        upit1 = "SELECT espb FROM predmeti WHERE id=%s"
        vrednost1 = (predmet_id['predmet_id'],)
        kursor.execute(upit1, vrednost1)
        espb_predmeta = kursor.fetchone()
        # racunam novi espb
        upit2 = "SELECT espb FROM studenti WHERE id=%s"
        vrednost2 = (id1,)
        kursor.execute(upit2, vrednost2)
        stari_espb = kursor.fetchone()
        # ako je ocena 5 onda ne diramo espb
        upit="SELECT ocena FROM ocene WHERE id=%s"
        vrednost=(id,)
        kursor.execute(upit,vrednost)
        ocena=kursor.fetchone()
        if int(ocena['ocena'])<6:
            novi_espb = str(stari_espb['espb'])
        else:
            novi_espb = int(stari_espb['espb']) - int(espb_predmeta['espb'])
        # brisanje ocene iz tabele ocene
        upit3 = "DELETE FROM ocene WHERE id=%s"
        vrednost3 = (id,)
        kursor.execute(upit3, vrednost3)
        konekcija.commit()
        # nova prosecna ocena
        upit4 = "SELECT AVG(ocena) FROM ocene WHERE student_id=%s and ocena>5"
        vrednost4 = (id1,)
        kursor.execute(upit4, vrednost4)
        novi_prosek = kursor.fetchone()
        # update proseka i espb
        if novi_prosek['AVG(ocena)'] == None:
            upit5 = "UPDATE studenti SET espb=0, prosek_ocena=0 WHERE id=%s"
            vrednost5 = (id1,)
            kursor.execute(upit5, vrednost5)
            konekcija.commit()
        else:
            upit5 = "UPDATE studenti SET espb=%s, prosek_ocena=%s WHERE id=%s"
            vrednosti5 = (str(novi_espb), str(novi_prosek['AVG(ocena)']), id1)
            kursor.execute(upit5, vrednosti5)
            konekcija.commit()
        # poruka o uspesnosti
        flash('Uspešno ste obrisali ocenu!', 'ocena')
        return redirect(url_for('studentt', id=id1))
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


@app.route('/ocena_izmena/<id>/<id1>', methods=['GET', 'POST'])
def ocena_izmena(id, id1):
    if ulogovan():
        if request.method == 'GET':
            upit = "SELECT predmet_id FROM ocene WHERE id=%s"
            vrednost=(id,)
            kursor.execute(upit,vrednost)
            predmet_id = kursor.fetchone()
            upit="SELECT naziv FROM predmeti WHERE id=%s"
            vrednost=(predmet_id['predmet_id'],)
            kursor.execute(upit, vrednost)
            predmet=kursor.fetchone()
            upit1 = "SELECT * FROM ocene WHERE id=%s"
            vrednost = (id,)
            kursor.execute(upit1, vrednost)
            ocena = kursor.fetchone()
            return render_template('ocena_izmena.html',predmet_id=predmet_id, id2=id, stid=id1, predmeti=predmet, ocena=ocena)
        elif request.method == 'POST':
            forma = request.form
            upit = """UPDATE ocene
						SET ocena=%s, datum=%s
						WHERE id=%s
					"""
            vrednosti = (forma['ocena'], forma['datum'], id)
            kursor.execute(upit, vrednosti)
            konekcija.commit()
            # resavanje espb
            # prvo trazim stari espb
            upit = "SELECT espb FROM studenti WHERE id=%s"
            vrednosti = (id1,)
            kursor.execute(upit, vrednosti)
            stari_espb = kursor.fetchone()
            # trazim espb za odabrani predmet
            upit = "SELECT espb FROM predmeti WHERE id=%s"
            vrednosti = (forma['izbor'],)
            kursor.execute(upit, vrednosti)
            predmet_espb = kursor.fetchone()
            # dobijanje novog espb
            if int(forma['ocena']) == 5:
                novi_espb = int(stari_espb['espb']) - int(predmet_espb['espb'])
            else:
                novi_espb = int(stari_espb['espb'])
                # resavanje prosecne ocene
                # napomena: vec smo uneli novu ocenu u bazu
            upit = "SELECT AVG(ocena) FROM ocene WHERE student_id=%s AND ocena>5"
            vrednosti = (id1,)
            kursor.execute(upit, vrednosti)
            novi_prosek = kursor.fetchone()
            # unos novih u bazu
            upit1 = "UPDATE studenti SET espb=%s, prosek_ocena=%s WHERE id=%s"
            vrednosti = (str(novi_espb), str(novi_prosek['AVG(ocena)']), id1)
            kursor.execute(upit1, vrednosti)
            konekcija.commit()
            flash('Uspešna izmena ocene!', 'ocena')
            return redirect(url_for('studentt', id=id1))
    else:
        flash('Morate se ulogovati da bi pristupili resursima ove stranice !', 'resurs')
        return redirect(url_for('login'))


app.run(debug=True, port='8000')
