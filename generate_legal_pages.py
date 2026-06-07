import os

template_file = 'legal.template.html'

pages = {
    'about.html': {
        'title': 'About the Investigative Dossier',
        'header': 'PROSPECTUS',
        'content': '''
            <p>Welcome to the central node of the Death Note Investigative Dossier. This platform serves as a high-fidelity digital archive for the events surrounding the Kira investigation. Our mission is to provide an immersive, high-performance portal for researchers and fans alike to study the psychological warfare between Light Yagami and L Lawliet.</p>
            <h2>THE ARCHIVE</h2>
            <p>Our database contains all 108 primary case files (chapters), optimized with next-gen AVIF/WebP imagery and sub-second loading performance. We utilize a Gothic Noir architecture to maintain the atmospheric integrity of the original documents.</p>
            <h2>JUSTICE</h2>
            <p>Whether you follow the cold logic of Investigative Mode (L) or the radical vision of God of New World Mode (Kira), this archive remains neutral, providing the raw evidence for your own conclusions.</p>
        '''
    },
    'contact.html': {
        'title': 'Contact the Task Force',
        'header': 'COMMUNICATIONS',
        'content': '''
            <p>Secure lines are open for inquiries, feedback, or reporting anomalies in the archive. Please use the cryptic channels provided below.</p>
            <h2>SECURE CONTACT</h2>
            <p>Email: taskforce@deathnote-online.com</p>
            <p>Note: All communications are monitored by Watari. Do not reveal your true name if you suspect you are being watched.</p>
            <h2>TECHNICAL SUPPORT</h2>
            <p>For issues regarding page rendering or performance, please include your browser's metadata in the report.</p>
        '''
    },
    'privacy-policy.html': {
        'title': 'Privacy Policy',
        'header': 'DATA RETENTION',
        'content': '''
            <p>We respect your anonymity. Unlike the Shinigami Eyes, we do not require your name or lifespan to grant access to this portal.</p>
            <h2>INFORMATION COLLECTION</h2>
            <p>This site is a static archive. We do not use databases to store personal user information. Standard logging for performance monitoring may occur but is kept strictly confidential within the task force.</p>
        '''
    },
    'dmca.html': {
        'title': 'DMCA Policy',
        'header': 'INTELLECTUAL PROPERTY',
        'content': '''
            <p>This portal is an educational and fan-driven archive dedicated to the study of the Death Note series. We claim no ownership over the original intellectual property created by Tsugumi Ohba and Takeshi Obata.</p>
            <h2>REPORTING INFRINGEMENT</h2>
            <p>If you represent the legal owners of the series and wish for certain files to be retracted, please send a formal DMCA notice to dmca@deathnote-online.com. We respond to all valid requests within 48 investigative hours.</p>
        '''
    },
    'terms.html': {
        'title': 'Terms of Use',
        'header': 'CODE OF CONDUCT',
        'content': '''
            <p>By accessing this dossier, you agree to the conditions set forth by the Kira Task Force. Failure to comply may result in removal from the safe-network.</p>
            <h2>USAGE LIMITS</h2>
            <p>Users are encouraged to study the materials for personal use. Automated scraping or mass-cloning of this archive is strictly prohibited without authorization from Watari.</p>
            <h2>DISCLAIMER OF LIABILITY</h2>
            <p>The Task Force is not responsible for any psychological impact resulting from the study of the Death Note. Access at your own analytical risk.</p>
        '''
    },
    'cookies.html': {
        'title': 'Cookie Policy',
        'header': 'SESSION MARKERS',
        'content': '''
            <p>This site uses minimal cookies to enhance your investigative experience.</p>
            <h2>USE OF COOKIES</h2>
            <p>Cookies are used to remember your preferred mode (L or Kira) across different chapters. This ensures your atmospheric settings remain stable during long research sessions.</p>
            <h2>MANAGING SETTINGS</h2>
            <p>You can disable cookies in your browser, but your mode preference will reset to default upon each page load.</p>
        '''
    },
    'disclaimer.html': {
        'title': 'Disclaimer',
        'header': 'THEORETICAL FRAMEWORK',
        'content': '''
            <p>The content within this portal is intended for entertainment and analysis purposes only. The "Death Note" is a fictional concept; any attempt to recreate the phenomena described in the manga is inherently impossible.</p>
            <h2>REAL-WORLD NAMES</h2>
            <p>Any resemblance to real-world names or entities is purely coincidental, as documented in the original creative works.</p>
        '''
    }
}

def generate_pages():
    if not os.path.exists(template_file):
        print(f"Error: {template_file} not found.")
        return

    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()

    for filename, data in pages.items():
        html = template.replace('{title}', data['title'])
        html = html.replace('{header}', data['header'])
        html = html.replace('{content}', data['content'])
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Generated {filename}")

if __name__ == "__main__":
    generate_pages()
