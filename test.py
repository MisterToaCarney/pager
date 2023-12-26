import postprocess
from postprocess.flex_next import ParsedFlexPage

i = 0
result_count = 0
result_no_gc_count = 0
mismatch_count = 0

with open("pager.log", "br") as f:
  for line in f.readlines():
    i += 1
    unparsed_page = line.decode()
    if not "(Part" in unparsed_page: continue
    parsed_page = postprocess.parse_page(unparsed_page)

    if not parsed_page: continue

    # print(parsed_page)


    if isinstance(parsed_page, ParsedFlexPage):
      result = postprocess.fire.defrag_fire_page(parsed_page)

      if result: 
        result_count += 1
        print(result.message)
        print()

    if i >= 129626:
      pass

print("Result Count", result_count)
print("Result no gc count", result_no_gc_count)
print("Mismatch count", mismatch_count)
print("Lines processed", i)



