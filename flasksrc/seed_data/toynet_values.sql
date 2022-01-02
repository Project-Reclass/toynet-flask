-- This file is part of Toynet-Flask.
-- 
-- Toynet-Flask is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
-- 
-- Toynet-Flask is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
-- 
-- You should have received a copy of the GNU General Public License
-- along with Toynet-Flask.  If not, see <https://www.gnu.org/licenses/>.

/*
NOTE: We should create an enum for the military branches

INSERT INTO toynet_value(id, name) VALUES(####, "Value Name");
INSERT INTO toynet_value_inspiration(value_id, organization, quote) VALUES(####, "Org Name 1", "Org Quote 1");
INSERT INTO toynet_value_inspiration(value_id, organization, quote) VALUES(####, "Org Name 2", "Org Quote 2");
*/

BEGIN TRANSACTION;

INSERT INTO toynet_values(id, name) VALUES(5001, "Integrity");
INSERT INTO toynet_value_inspirations(value_id, organization, quote) VALUES(5001, "U.S. Air Force", "Integrity is the adherence to a strong moral code and consistency in one’s actions and values [...] Airmen should be guided by a deeply held sense of honor, not one of personal comfort or uncontrolled selfish appetites.");
INSERT INTO toynet_value_inspirations(value_id, organization, quote) VALUES(5001, "U.S. Army", "Do what is right, legally and morally. Integrity is a quality you develop by adhering to moral principles. It requires that you do and say nothing that deceives others. As your integrity grows, so does the trust others place in you [...] and, finally, the fundamental acceptance of yourself.");
INSERT INTO toynet_value_inspirations(value_id, organization, quote) VALUES(5001, "U.S. Coast Guard", "Integrity is our standard. We demonstrate uncompromising ethical conduct and moral behavior in all of our personal actions. We are loyal and accountable to the public trust.");

INSERT INTO toynet_value_entries(value_id, username, user_group_id, quote) VALUES(5001, "tay@projectreclass.org", "ALPHA", "In my opinion, integrity is completeness and consistency.");
INSERT INTO toynet_value_entries(value_id, username, quote) VALUES(5001, "bot@projectreclass.org", "Bots do not need integrity.");

INSERT INTO toynet_values(id, name) VALUES(5002, "Respect");
INSERT INTO toynet_value_inspirations(value_id, organization, quote) VALUES(5002, "U.S. Army", "Treat people as they should be treated [...] Respect is what allows us to appreciate the best in other people. Respect is trusting that all people have done their jobs and fulfilled their duty.");

INSERT INTO toynet_values(id, name) VALUES(5003, "Honor");
INSERT INTO toynet_value_inspirations(value_id, organization, quote) VALUES(5003, "U.S. Army", "Live up to Army values [...] Honor is a matter of carrying out, acting, and living the values of respect, duty, loyalty, selfless service, integrity and personal courage in everything you do.");
INSERT INTO toynet_value_inspirations(value_id, organization, quote) VALUES(5003, "U.S. Marines", "The quality of maturity, dedication, trust, and dependability that commits Marines to act responsibly; to be accountable for actions; to fulfill obligations; and to hold others accountable for their actions.");

INSERT INTO toynet_values(id, name) VALUES(5004, "Loyalty");
INSERT INTO toynet_value_inspirations(value_id, organization, quote) VALUES(5004, "U.S. Army", "Bear true faith and allegiance to the U.S. Constitution, the Army, your unit and other Soldiers. Bearing true faith and allegiance is a matter of believing in and devoting yourself to something or someone … By wearing the uniform of the U.S. Army you are expressing your loyalty. And by doing your share, you show your loyalty to your unit.");

END TRANSACTION;
