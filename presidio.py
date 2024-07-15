from presidio_analyzer import AnalyzerEngine

#text = "His name is Mr. Jones and his phone number is 212-555-5555"
"""text = John Smith received a notification on his phone about a suspicious login attempt to his 
        bank account number 123456785678. The message included his home address at 123 Maple Street and 
        advised him to change his password immediately. Concerned about his security, John accessed 
        his medical records, which contained his birth date, April 5, 1985, and biometric data such 
        as retina scans. He also found an email from his health insurance provider that contained his 
        Social Security Number. In a rush, John sent a text message to his wife, including their 
        daughter’s recent school photo, which inadvertently showed their home address in the background"""

text = """
Rajesh Kumar noticed an unexpected transaction in his savings account, numbered 9876543210, 
at State Bank of India. He immediately called the bank's customer service from his mobile number, 
+91 98765 43210, to report the issue. While on hold, he received an email from his credit card company 
at his email address, rajesh.kumar@example.com, indicating a potential breach. The email contained his 
home address, 1234, MG Road, Bengaluru, Karnataka, 560001, and advised him to review recent transactions.
In a state of panic, Rajesh checked his saved passwords and PINs document on his computer, 
which included his birth date, 15 August 1985, and discovered that his Aadhaar Number, 1234 5678 9012, 
was also listed there. He quickly updated his security settings and changed all his passwords to protect 
his accounts
"""

analyzer = AnalyzerEngine()
analyzer_results = analyzer.analyze(text=text, language="en")

print(analyzer_results)