def find_kth_number(k):
    # Ketma-ket sonlar ketma-ketligini hosil qilish
    num = 11  # Dastlabki son
    count = 0  # Nechanchi raqam ekanligini hisoblash
    while True:
        num_str = str(num)  # Sonni satrga aylantiramiz
        count += len(num_str)  # Raqamning uzunligini qo'shamiz
        if count >= k:  # Agar k-pozitsiya raqamga yetib borgan bo'lsak
            return num_str[k - (count - len(num_str)) - 1]  # K-pozitsiya raqamni qaytarish
        num += 1  # Keyingi sonni tekshirish

# Misol: K-pozitsiyadagi raqamni topamiz
k = 20  # Misol uchun k = 20
result = find_kth_number(k)
print(f"{k}-pozitsiyadagi raqam: {result}")
